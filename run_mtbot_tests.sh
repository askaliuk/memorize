# Run specific test module
# python -m unittest mtbot.test.test_simple
# Run specific test method
# python -m unittest mtbot.test.test_simple.TestSimple.test_simple
# Run all mtbot tests
python -m unittest discover -s mtbot/test -t . -v