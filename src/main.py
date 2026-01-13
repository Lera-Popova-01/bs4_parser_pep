import re
import requests_cache
import logging

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm

from constants import BASE_DIR, MAIN_DOC_URL, PEP_URL, EXPECTED_STATUS
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(soup, 'div', attrs={'role': 'main'})
    table_tag = find_tag(main_tag, 'table', attrs={'class': 'docutils'})
    zip_tag = find_tag(table_tag, 'a', attrs={'href': re.compile(r'.+zip$')})
    zip_link = zip_tag['href']
    archive_url = urljoin(downloads_url, zip_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def get_status(dl_tag):
    dt_tags = dl_tag.find_all('dt')
    for dt in dt_tags:
        if dt.get_text(strip=True).startswith('Status'):
            dd = dt.find_next_sibling('dd')
            if dd:
                abbr = dd.find('abbr')
                if abbr:
                    return abbr.get_text(strip=True)
                else:
                    return dd.get_text(strip=True).strip()
    return None


def pep(session):
    response = get_response(session, PEP_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    section_pep_list = find_tag(
        soup, 'section', attrs={'id': 'index-by-category'}
    )
    tr_tags = section_pep_list.select('section tbody tr')
    status_counts = {}
    results = [['Статус', 'Количество']]
    total_pep = 0
    mismatched_statuses = []
    for tr_tag in tqdm(tr_tags):
        td_tags = tr_tag.find_all('td')
        td_tag = td_tags[0].text[1:].strip()
        total_pep += 1
        a_tag = find_tag(td_tags[1], 'a')
        pep_link = a_tag['href']
        pep_url = urljoin(PEP_URL, pep_link)
        response_pep = get_response(session, pep_url)
        if response_pep is None:
            return
        soup_pep = BeautifulSoup(response_pep.text, 'lxml')
        dl_tag = find_tag(
            soup_pep, 'dl', attrs={'class': 'rfc2822 field-list simple'}
        )
        dd_status = get_status(dl_tag)
        if dd_status is None:
            continue
        if dd_status not in status_counts:
            status_counts[dd_status] = 0
        status_counts[dd_status] += 1
        expected_statuses = EXPECTED_STATUS.get(td_tag, ())
        if dd_status not in expected_statuses:
            mismatched_statuses.append({
                'url': pep_url,
                'pep_status': td_tag,
                'page_status': dd_status
            })
        for status, count in status_counts.items():
            results.append([status, count])
        results.append(['Total', total_pep])
    if mismatched_statuses:
        logging.info('Несовпадающие статусы:')
        for item in mismatched_statuses:
            print(f"\n{item['url']}")
            print(f"Статус в карточке: {item['page_status']}")
            print(f"Ожидаемые статусы: {list(EXPECTED_STATUS.get(
                item['pep_status'][0], ()
            ))}")
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
