from utils import File, Log

from ballot.Candidate import Candidate

log = Log('ReadMe')


class ReadMe:
    PATH = 'README.md'

    def build(self):
        lines = [
            '# The Candidates',
            '',
            '## 2024 Sri Lankan Presidential Election',
            '',
            '| Symbol | Candidate Name | ... |',
            '|--:|:--|---|',
        ]

        candidate_list = Candidate.list_all()
        for candidate in candidate_list:
            lines.append(candidate.readme_row)

        File(self.PATH).write('\n'.join(lines))
        log.info(f'Wrote {self.PATH}')


if __name__ == '__main__':
    ReadMe().build()
