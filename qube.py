import collections
import math
import itertools

class mdq:
    def __init__(self) -> None:
        """
        Expects a dictionary in the form {'dimension_name':['dimension_attributes']}
        There must be one dimensions called Values that has at minimum a single attribute.

        so the minimal definiton is for example {"Values", "Data"}
        """
        self.dims = {}
        self.dimIndex = {}
        self.dimReverseIndex = {}
        self.data = []
        self.strides = {}
        self.VNAME = "Values"

    def setDims(self, dimensions : dict) -> None:
        if self.VNAME not in dimensions:
            raise ValueError ("Expected a dimension called value")
        if len(dimensions[self.VNAME]) == 0:
            raise ValueError ("Value Dimension must have one attribute")
        
        #set up core dimensions and indices
        #TODO move Values to the end, but it shoudn't matter where it is
        for name, attributes in dimensions.items():
            self.dims[name] = tuple(dict.fromkeys(attributes))
            positions = enumerate(self.dims[name])
            self.dimIndex[name] = {v : p for p, v in positions}
            self.dimReverseIndex[name] = {p : v for p, v in positions}       
        
        #build data matrix & strides
        cells = 1
        
        for attributes in self.dims.values():
            cells = cells * len(attributes)
        self.data = [None]*cells



        def strider(lst):
            if not lst:
                #print('f', lst)
                return [1]
            else:
                #print('q', lst[0], lst[1:])
                out = strider(lst[1:])
                return [lst[0] * out[0]] + out 
    
        sizes = [len(attributes) for attributes in self.dims.values()]
        strides = strider(sizes)[1:]
        self.strides = {k:v for k,v in zip(self.dims.keys(),strides )}

       
       
                      
    def __str__(self) -> str:
        out = {"Dims": self.dims.keys(), "Strides": self.strides, "Data": self.data}
        out = [f"  -{k}: {v}" for k,v in out.items()]
        return "\n".join(out)
    
    def getIndex(self, dims_addr: dict) -> int:
        if self.isAddress(dims_addr):
            index = [(dim, self.strides[dim], self.dimIndex[dim][attr]) for dim, attr in dims_addr.items()]
            index = sum(map(lambda x: x[1] * x[2], index))
            return index
        else:
            return -1
    
    def setValue(self, dims_addr: dict, value) -> None:
        #calculate value index
        self.data[self.getIndex(dims_addr)] = value

    def getValue(self, dims_addr: dict):
        return self.data[self.getIndex(dims_addr)]

    def isAddress(self, dims_addr: dict) -> bool:
        # check address is complete
        for name in self.dims.keys():
            if name not in dims_addr:
                raise ValueError(f"Dimension {name} is not in the value address")
            if dims_addr[name] not in self.dims[name]:
                raise ValueError(f"Attribute {dims_addr[name]} is not a valid attribute of {name} ")
        return True    

class QubeViewer:
    def __init__(self, qube: mdq) -> None:
        self.q = qube
        self.view = None
    
    def getDefaultView(self):
        out = {"cols": self.q.dims, "rows":self.q.dims }
        return out
    
    def toString(self) -> str:
        out =  ["An Enigmantic Multidimensional cube:"]

        if self.view is None:
            viewspec = self.getDefaultView()
        else:
            viewspec = self.view
        
        #header
        out.append(str(tuple(viewspec["cols"].keys())))
        out += [str(tuple(viewspec["cols"].values())) for _ in viewspec["rows"]]

        return "\n".join(out)

class Qube:
    
    def __init__(self, dimensions) -> None:
        self.q = mdq()
        self.q.setDims(dimensions)
        self.view = QubeViewer(self.q)
        

    def __str__(self) -> str:
        return self.view.toString()
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def setValue(self, dims_addr: dict, value) -> None:
        self.q.setValue(dims_addr, value)

    def getValue(self, dims_addr: dict):
        return self.q.getValue(dims_addr)


        

    





# class Mdim():
    
        





    

        

#     def getValue(self, path):
#         list_path = [(k,v) for k,v in path.items()]
#         return self._getValue(list_path, self.values)




#     def __str__(self):
#         out = []

#         header = "\t".join(list(self.dims.keys())+["Values"])
#         out.append(header)

#         rows = list(itertools.product(*self.dims.values()))

#         tmp =[]
#         for row in rows:
#             path = {tuple(self.dims.keys())[i]: row[i] for i in range(len(row))}
#             value = self.getValue(path)
#             value = value if value is not None else "None"
#             elements = list(row)
#             elements.append(value)
#             new_row = "\t".join(map(str,elements))
#             tmp.append(new_row)

#         #rows = ["\t".join(map(str, row)) for row in rows] - nice version
#         out += tmp
#         return "\n".join(out)

#     def print(self):
#         print(self.__str__)














 




