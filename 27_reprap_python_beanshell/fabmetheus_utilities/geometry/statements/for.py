"""
Polygon path.

"""

from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities.geometry.geometry_utilities import evaluate


__author__ = "Enrique Perez (perez_enrique@yahoo.com)"
__credits__ = 'Art of Illusion <http://www.artofillusion.org/>'
__date__ = "$Date: 2008/02/05 $"
__license__ = "GPL 3.0"


def processChildrenByIndexValue( function, index, indexValue, value, xmlElement ):
	"Process children by index value."
	function.localDictionary[ indexValue.indexName ] = index
	function.localDictionary[ indexValue.valueName ] = value
	function.processChildren( xmlElement )

def processXMLElement( xmlElement, xmlProcessor ):
	"Process the xml element."
	if xmlElement.object == None:
		xmlElement.object = IndexValue( xmlElement )
	if xmlElement.object.inSplitWords == None:
		return
	if len( xmlProcessor.functions ) < 1:
		print( 'Warning, "for" element is not in a function in processXMLElement in for.py for:' )
		print( xmlElement )
		return
	function = xmlProcessor.functions[ - 1 ]
	inValue = evaluate.getEvaluatedExpressionValueBySplitLine( xmlElement.object.inSplitWords, xmlElement )
	if inValue.__class__ == list:
		for index, value in enumerate( inValue ):
			processChildrenByIndexValue( function, index, xmlElement.object, value, xmlElement )
		return
	if inValue.__class__ == dict:
		inKeys = inValue.keys()
		inKeys.sort()
		for inKey in inKeys:
			processChildrenByIndexValue( function, inKey, xmlElement.object, inValue[ inKey ], xmlElement )


class IndexValue:
	"Class to get the in attribute, the index name and the value name."
	def __init__( self, xmlElement ):
		"Initialize."
		self.inSplitWords = None
		self.indexName = '_index'
		if 'index' in xmlElement.attributeDictionary:
			self.indexName = xmlElement.attributeDictionary[ 'index' ]
		self.valueName = '_value'
		if 'value' in xmlElement.attributeDictionary:
			self.valueName = xmlElement.attributeDictionary[ 'value' ]
		if 'in' in xmlElement.attributeDictionary:
			self.inSplitWords = evaluate.getEvaluatorSplitWords( xmlElement.attributeDictionary[ 'in' ] )
		else:
			print( 'Warning, could not find the "in" attribute in IndexValue in for.py for:' )
			print( xmlElement )
			return
		if len( self.inSplitWords ) < 1:
			self.inSplitWords = None
			print( 'Warning, could not get split words for the "in" attribute in IndexValue in for.py for:' )
			print( xmlElement )
