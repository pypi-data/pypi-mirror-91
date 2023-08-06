try:
    ie6 = None
    import PySide6 as QtFramework
    from QtFramework import QtCore
    Slot = QtCore.Slot
except ImportError as err:
    ie6 = err
    print (ie6)
except ModuleNotFoundError as err:
    ie6 = err
    print (ie6)
if ie6 is not None:
    try:
        print ("Try PySide2")
        ie2 = None
        import PySide2
        import PySide2 as QtFramework
        from PySide2 import QtCore
        Slot = QtCore.Slot
    except ImportError as err:
        ie2 = err
        print (ie2)
    except ModuleNotFoundError as err:
        err = ie2
        print (ie2)
    if ie2 is not None:
        try:
            ie5 = None
            import PyQt5 as QtFramework
            from QtFramework import QtCore
            Slot = QtCore.pyqtslot
        except ImportError as err:
            ie5 = err
            print (ie5)
        except ModuleNotFoundError as err:
            ie5 = err
            print (ie5)
        if ie5 is not None:
            raise ImportError('Could not import any Qt Framework out of PySide6, PySide2, PyQt5')
