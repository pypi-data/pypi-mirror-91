# pspring

This is a lightweight framework to enable python developers to quickly develop apps with annotations/decorators. Inspired by Spring Framework of Java, the framework provides the ability for IOC ( Inversion of control ) and Autowiring the beans.

The default environment variables can always be found `defaultvars.py` file

Below is the index the annotations/decorators supported by this module

* `@Bean(name="")`

  This decorator will register the class or method ( which returns an instance of bean ) to the pspring application context. You can provide an optional `name` attribute to register the bean with a qualified name. Providing no name would register the bean for its type ( and its base classes )


* `@Autowired(name=beanname)`

  This decorator is the heard of dependency injection and will autowire the arguments of a method ( especially used in `__init__` constructor ). You can provide a list of name value pairs where, `name` is the argument name in the method definition for which a bean named `beanname` would be injected with that qualifier.

## Configuration Framework

Configuring applications can get complicated with environment variables, default variables and various source of configurations ( like secrets, encrypted variables etc ).

pspring brings a configuration framework which can be used exhaustively for developing cloud applications. The idea in Configuration framework is to provide a standard interface for applications to fetch properties.

The two classes which forms the backbone of this framework are `Configuration` and `ConfigurationProvider`. During the application start up, the framework needs to be initialized with a list of ConfigurationProviders as shown below

```python

from pspsring import Configuration, ConfigurationProvider

config = {
	"firstname" : "dave",
	"lastname" : "picaso"
}

# A simple dictionary based config provider
class DictionaryConfigurationProvider(ConfigurationProvider):
	def getProperty(propertyName):
		return config.get(propertyName)

Configuration.initialize([
	DictionaryConfigurationProvider()
])

config = Configuration.getConfig(__name__)

# will print 'dave'
print(config.getProperty("firstname"))


```

Within a module, the configuration provides a means for namespace to avoid property name conflicts.

Example:
```python

from pspsring import Configuration
config = Configuration.getConfig(__name__)

print(config.getProperty("firstname"))

```

In the above code, we create a configiration accessor instance by passing in the module name ( __name__ ). This will create a namespace under which the property lives. For Eg: if the file is saved under the package as com/example/application.py, the property name will be actually referenced as `com.example.application.firstname`.

when getProperty method is invoked

	1) the property is looked up in environment variables
	2) the property is searched in the given list of ConfigurationProviders during initialization
	3) the property is searched in the defaults
	4) Search the property one above the hierarchy in the namespace starting from step 1. ( Eg: com.example.firstname )

The above search sequence is pursued until the property is found. If the property is not found,then `None` is returned.

pspring along with pspring-aws provides a wealth of ConfigurationProviders ( SecretsMgrConfigProvider, DynamodbConfigProvider, RealTimeSecretsMgrConfigProvider etc...) that can be used with aws.

## Usage

The context of pspring should be initialized before any dependency injection is expected. A sample of code is show below

```python
import sys,os

from pspring import *

config = Configuration.getConfig(__name__)

@Bean(name="loggerBeanName")
class Logger():
  def __init__():
    pass

  def sayHi(self,name):
    print("Hi "+str(name));

class MyApp():
  @Autowired(mylogger="loggerBeanName")
  def __init__(self,mylogger:Logger):
    self.logger = mylogger

os.environ["name"] = "dave"

Configuration.initialize([])

ApplicationContext.initialize()


app = MyApp()

# prints "Hi dave"
app.logger.sayHi(config.getProperty("name"))
```
