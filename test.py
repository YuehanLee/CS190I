#!/usr/bin/env python
import math
import tyrell.spec as S
from tyrell.interpreter import PostOrderInterpreter
from tyrell.enumerator import SmtEnumerator, RelaxedRandomEnumerator
from tyrell.decider import Example, ExampleConstraintDecider, ExampleConstraintPruningDecider
from tyrell.synthesizer import Synthesizer
from tyrell.logger import get_logger

logger = get_logger('tyrell')

class ToyInterpreter(PostOrderInterpreter):

    def eval_get_int(self, node, args):
        return int(args[0])

    def eval_plus(self, node, args):
        return args[0] + args[1]

    def eval_mult(self, node, args):
        return args[0] * args[1]

    def eval_power(self, node, args):
        if(args[0] >= 10 or args[1] >= 10):
            return 0
        return pow(args[0], args[1])

    def eval_fac(self, node, args):
        if(args[0]>=7):
            return 0
        return math.factorial(args[0])


def main():
    logger.info('Parsing Spec...')
    # TBD: parse the DSL definition file and store it to `spec`
    #spec = ??
    spec = S.parse_file('example/test.tyrell')
    logger.info('Parsing succeeded')

    logger.info('Building synthesizer...')
    synthesizer = Synthesizer(
        enumerator=SmtEnumerator(spec, depth=4, loc=4),
        decider=ExampleConstraintDecider(
            spec=spec, # TBD: provide the spec here
            interpreter=ToyInterpreter(),
            examples=[
                Example(input=[1], output=4),
                Example(input=[2], output=8),
                Example(input=[3], output=16),
                Example(input=[4], output=32),
                ] # TBD: provide the example here
        )
    )
    logger.info('Synthesizing programs...')

    prog = synthesizer.synthesize()
    if prog is not None:
        logger.info('Solution found: {}'.format(prog))
    else:
        logger.info('Solution not found!')


if __name__ == '__main__':
    logger.setLevel('DEBUG')
    main()
