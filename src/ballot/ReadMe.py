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
            '### Major Candidates †',
            '',
            '| Symbol | Candidate Name | ... |',
            '|--:|:--|---|',
        ]

        candidate_list = Candidate.list_all()
        for candidate in candidate_list:
            if candidate.is_major:
                lines.append(candidate.readme_row)

        lines.extend(
            [
                '',
                '> †Candidates or Candidates Representing Parties that have won at least 1% of the vote in a Presidential Election in the past 15 years, or polled at least 10% of the predicted voting share in a recognized election poll, at the close of nominations. Yo, or somethin\' like that, you feel me? You know what I\'m sayin...',
                '',
                '### Other Candidates',
                '',
                '| Symbol | Candidate Name | ... |',
                '|--:|:--|---|',
            ]
        )

        for candidate in candidate_list:
            if not candidate.is_major:
                lines.append(candidate.readme_row)

        File(self.PATH).write('\n'.join(lines))
        log.info(f'Wrote {self.PATH}')


if __name__ == '__main__':
    ReadMe().build()
