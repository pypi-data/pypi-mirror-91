############################
tinyCrawl Documentation
############################

该项目为BBD自有的模型全流程再封装的module包，通过直接调用包中的各类再封装的函数，主要有以下作用：

- 杜绝重复造轮子，减少代码时间
- 对建模流程的代码进行标准化，统一各类结果输出的格式
- 通过调用标准的再封装功能函数，避免项目中自写的代码中存在失误、错误代码等。
- 对使用的第三方包的版本进行统一管理和标准化，避免因部署环境不同、项目交接引起的包版本不一致造成的代码不兼容等问题

`项目地址 <http://git.bbdops.com/BBD_MODEL_standard_module/bbdmodeling>`_

.. toctree::
  :caption: 使用指南
  :maxdepth: 2

  install/index
  howtouse/index
  example/index

.. toctree::
  :caption: API
  :maxdepth: 2

  api/index
