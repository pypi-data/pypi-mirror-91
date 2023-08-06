import inspect
import sys, types

def _get_mod(modulePath):
  try:
    aMod = sys.modules[modulePath]
    if not isinstance(aMod, types.ModuleType):
      raise KeyError
  except KeyError:
    # The last [''] is very important!
    aMod = __import__(modulePath, globals(), locals(), [''])
    sys.modules[modulePath] = aMod
  return aMod

def _get_func(fullFuncName):
  """Retrieve a function object from a full dotted-package name."""
  # Parse out the path, module, and function
  lastDot = fullFuncName.rfind(u".")
  funcName = fullFuncName[lastDot + 1:]
  modPath = fullFuncName[:lastDot]
  aMod = _get_mod(modPath)
  aFunc = getattr(aMod, funcName)
  # Assert that the function is a *callable* attribute.
  assert callable(aFunc), u"%s is not callable." % fullFuncName
  # Return a reference to the function itself,
  # not the results of the function.
  return aFunc


def _get_Class(fullClassName, parentClass=None):
  """Load a module and retrieve a class (NOT an instance).
  If the parentClass is supplied, className must be of parentClass
  or a subclass of parentClass (or None is returned).
  """
  aClass = _get_func(fullClassName)
  # Assert that the class is a subclass of parentClass.
  if parentClass is not None:
    if not issubclass(aClass, parentClass):
      raise TypeError(u"%s is not a subclass of %s" %
              (fullClassName, parentClass))
  # Return a reference to the class itself, not an instantiated object.
  return aClass


# def applyFuc(obj,strFunc,arrArgs):
#   objFunc = getattr(obj, strFunc)
#   # return apply(objFunc,arrArgs)
#   return apply(objFunc,arrArgs)


def getObject(fullClassName):
  clazz = _get_Class(fullClassName)
  return clazz()
if __name__=='__main__':
  # user=getObject("model2.user_main.UserMain")
  # # bb=applyFuc(aa, "select", ['select * from ngsys2',None])
  #
  # list = dir(user)
  # for i in list:
  #   # print("methond==={0}".format(i))
  #   if str(i).lower().strip().startswith("_api_"):
  #     print("methond==={0}".format(i))
  #
  # list2 = inspect.getmembers(user, predicate=inspect.ismethod)
  # for i in list2:
  #   if i[0].startswith("_api_"):
  #     # sig_func = inspect.signature(user.find_user)
  #     # print("function-parameter", sig_func.parameters)
  #     print("api_method", i[0])

  _model2_config = _get_func("model2.api_register.get_api_module")
  model2_api_modules = _model2_config()
  print("======>>>>", model2_api_modules)


  for m in model2_api_modules:
    user=getObject(m)
    # bb=applyFuc(aa, "select", ['select * from ngsys2',None])

    list = dir(user)
    for i in list:
      # print("methond==={0}".format(i))
      if str(i).lower().strip().startswith("_api_"):
        print("methond==={0}".format(i))

  # m = get_api_module()