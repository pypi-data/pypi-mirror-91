# pyloggerhelper

json格式log的帮助程序

## 使用

```python
from pyloggerhelper import log


def testrun():
    log.info("test")


if __name__ == "__main__":
    log.initialize_for_app("testapp")
    testrun()
```