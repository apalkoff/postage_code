from plumbum import cli
import logging

log = logging.getLogger(__name__)

class PostageCode:
    def __init__(self, postage_type, digits, country_code):
        assert len(postage_type) == 2
        assert len(digits) == 9
        assert len(country_code) == 2

        self.postage_type = postage_type
        self.country_code = country_code

        self.fill_digits(digits[:-1])

        assert str(self.check_digit) == digits[-1], 'Wrong check digit'

    def __str__(self):
        return f'{self.postage_type} {self.digits_str}{self.check_digit} {self.country_code}'

    @property
    def digits_str(self):
        return ''.join([str(d) for d in self.digits])

    @property
    def digits_int(self):
        return int(self.digits_str)

    @property
    def check_digit(self):
        multipliers =  [8, 6, 4, 2, 3, 5, 9, 7]
        assert len(multipliers) == len(self.digits)
        digit_sum = 0
        for i in range(len(multipliers)):
            digit_sum += multipliers[i]*self.digits[i]

        remainder = digit_sum % 11
        result = 11 - remainder

        if result == 10:
            return 0
        if result == 11:
            return 5
        return result

    def from_string(str_code):
        assert len(str_code) == 13
        postage_type = str_code[0:2]
        digits = str_code[2:-2]
        country_code = str_code[-2:]

        return PostageCode(postage_type, digits, country_code)

    def move_digits(self, diff):
        self.fill_digits(f'{self.digits_int + diff:08d}')

    def fill_digits(self, digits_str):
        self.digits = []

        for digit in digits_str:
            self.digits.append(int(digit))


class PostageApp(cli.Application):

    code = cli.SwitchAttr(
        ['-c', '--code'],
        str, default='',
        help="Postage code")

    before = cli.SwitchAttr(
        ['-b', '--before'],
        int, default=10,
        help="Number of postage codes before")

    after = cli.SwitchAttr(
        ['-a', '--after'],
        int, default=10,
        help="Number of postage codes after")

    def main(self):

        log.info('Start of postage')

        postage_code = PostageCode.from_string(self.code)
        print(f'Base postage_code: {postage_code}\n')

        for diff in range(-self.before, self.after):
            postage_code = PostageCode.from_string(self.code)
            postage_code.move_digits(diff)
            print(f'{diff:3d}: {postage_code}')

        if not self.code:
            log.critical('Please provide postage code')
            self.help()
            return 1

    @classmethod
    def run(cls, argv=None, exit=True):
        try:
            super(PostageApp, cls).run(argv=argv, exit=exit)
        except Exception as e:
            log.critical(e, exc_info=True)
            quit(1)

if __name__ == "__main__":
    PostageApp.unbind_switches('--help-all')
    PostageApp.run()