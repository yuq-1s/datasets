import tqdm
import csv
import logging
import fire

def filter_urls(filename, needed_language):
    with open(filename) as f:
        reader = csv.reader(f)
        for line in tqdm.tqdm(reader):
            try:
                url, language, forked_from = line[1], line[5], line[7]
            except (IndexError, ValueError):
                logging.debug(f"Ignoring {line}")
                continue
            if language == needed_language and forked_from == '\\N':
                yield url

def load_stars(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for line in tqdm.tqdm(reader):
            yield tuple(line)

def load_urls_in_language(filename):
    with open(filename) as f:
        for url in tqdm.tqdm(f):
            yield url

def main(action: str,
    language: str = "C",
    projects_filename: str = 'dump/projects.csv',
    min_star: int = 1000):
    assert action in ['language', 'star']
    repo_list_file = f'repos/repos_in_{language}.txt'
    if action == 'language':
        with open(repo_list_file, 'w') as f:
            for url in filter_urls(projects_filename, needed_language=language):
                try:
                    _, _, _, _, owner, repo = url.strip().split('/')
                except ValueError:
                    logging.debug(f"{url} parse failed")
                    continue
                f.write(f'{owner}/{repo}\n')
    elif action == 'star':
        star_count = dict(load_stars('data/repositories_small.csv'))
        with open(f'repos/repos_in_{language}_{min_star}_stars.txt', 'w') as f:
            for repo_id in load_urls_in_language(repo_list_file):
                repo_id = repo_id.strip()
                if repo_id not in star_count:
                    logging.debug(f"{repo_id} not found in stars counting")
                    continue
                if int(star_count[repo_id]) > min_star:
                    f.write(repo_id+'\n')
    else:
        assert False

if __name__ == '__main__':
    fire.Fire(main)