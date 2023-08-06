# Elements

## Overview
Element classes represent individual components of a web page. Form fields, Buttons, Links, Headers, Labels, Checkboxes, Radio Buttons, and all the other wonderful things that can be found on a web page are all represented by Element classes. 

Additionally, there are multiple abstract classes in this collection like ClickableElement and FormComponent which declare or implement functionality common to different classes of elements such as elements which can be clicked or elements which can be composed into forms.

Much like Page Object classes, Elements encapsulate the state, behavior, and performance characteristics of the web elements which they represent. The most important state variable in (almost) every Element class is the selector - the string containing XPATH or a CSS selector which can be used to locate any element of a particular type on any web page.

* The selector for each Element class is encapsulated in the `.selector()` method declared by the PageElement abstract class. It is unique for each Element class, and common to all instances of any particular Element class. For example, all instances of the Checkbox class have the same selector, but the Checkbox class has a different selector than every other Element class such as RadioButton.

	* There are two ways to locate an individual element on a web page:
	    * By Value-Attribute Pair: Instances of an element are often assigned unique identifiers of a certain attribute. Attributes can be anything, but the most often used ones are `id` and `class`. Automation Foundation can support any given attribute.
	        * Example: `Button(identifier="username_submit", attribute="id")`
	    * By XPath: Elements can alternatively be located by XPath. There are functions in Automation Foundation helpers/xpath_creation_functions to help form xpaths. This can be a more complicated way of searching for an element, but can be much more exact, and can be used for elements that don't have attributes to search on. XPaths can also more easily index commonly listed items.
	        * Example: `TableData(xpath="//tbody(@id='table_content')/tr[1]/td[3]")`
	        
	* The injection of the identifier into the selector happens automatically within the `.selector()` method - all you have to do as a test-writer is pass the identifer of any element you create to the element's constructor as a parameter.


