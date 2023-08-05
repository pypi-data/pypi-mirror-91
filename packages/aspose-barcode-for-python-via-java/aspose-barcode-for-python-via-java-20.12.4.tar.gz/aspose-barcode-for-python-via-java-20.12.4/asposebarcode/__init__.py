import jpype
import os
from asposebarcode import Generation, Recognition, Assist

__asposebarcode_dir__ = os.path.dirname(__file__)
__barcode_jar_path__ = __asposebarcode_dir__ + "/lib/aspose-barcode-python-20.12.jar"
jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % __barcode_jar_path__)
__all__ = ['Assist','Recognition','Generation','ComplexBarcode']