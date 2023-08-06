from james.utils import cmd


def test_cmd():
    assert cmd('echo foobar') == 'foobar'


def test_cmd_bool():
    assert cmd('echo foobar', return_success=True)
    assert not cmd('this command will fail', return_success=True)
