import collections
import math
import itertools
import returns

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
        self.values = {}

    def setDims(self, dimensions : dict, measures: dict) -> None:
        
        #set up core dimensions and indices
        for name, attributes in dimensions.items():
            self.dims[name] = tuple(dict.fromkeys(attributes))
            positions = enumerate(self.dims[name])
            self.dimIndex[name] = {v : p for p, v in positions}
            self.dimReverseIndex[name] = {p : v for p, v in positions}       
        
        #set up measures definiton
        #TODO validate measures
        self.values = measures
       
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
            out = index
        else:
            out = -1
        #print("getIndex:", out)
        return out
        
    def enumerateAddresses(self) -> list:
        """
        Returns a list of each cell's address in the cube
        """        
        dim = list(self.dims.keys())
        attributes = self.dims.values() 
        queries = [zip(dim, attributes) for attributes in itertools.product(*attributes)]
        queries = [{k:v for k,v in q} for q in queries ]

        out = queries

        # [{D1:V1, D2,V1 .. Dn, V1},{D1:V2, D2,V2 .. Dn, V2}...{Dn:Vx, D2,Vy .. Dn, Vz}]
        return queries


    
    def setValue(self, dims_addr: dict, value) -> None:
        #calculate value index
        self.data[self.getIndex(dims_addr)] = value

    def getValue(self, dims_addr: dict):
        out = self.data[self.getIndex(dims_addr)]
        #print("getValue:", out)
        return out

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
        cols = list(self.q.dims.keys()) + list(self.q.values.keys())
        out = {"cols": cols, "rows": None }
        return out
    
    def setView(self, rows: list, cols: list):
        viewspec = {"cols": cols, "rows": rows }
        self.view = viewspec

    
    def toString(self) -> str:
        def toHeaderStr(headers):
            return ",\t ".join(headers)

        def toDataStr(rows):
            out = []
            for row in rows:
                out.append(",\t".join([str(cell) for cell in row]))
            
            return "\n".join(out)


        if self.view is None:
            viewspec = self.getDefaultView()
        else:
            viewspec = self.view
        
        q = self.buildTable(viewspec)
        out = (
            f"{toHeaderStr(q["colHeader"])}\n"
            f"{toDataStr(q["dataBlock"])}\n"
        )
        return out
        #return "\n".join(self.buildTable(viewspec).values())
    
    def toHTML(self) -> str:
        def toHeaderStr(headers):
            out = [f"\t\t<th>{h}</th>" for h in headers] 
            return "\t<tr>\n" + "\n".join(out) + "\n\t</tr>\n"
        
        def toDataStr(rows):
            out = []
            for row in rows:
                rout = []
                for cell in row:
                    rout.append(f"\t\t<td>{cell}</td>")
                
                out.append("\t<tr>")
                out.append("\n".join(rout))
                out.append("\t</tr>")

            
            return "\n".join(out)

        
        if self.view is None:
            viewspec = self.getDefaultView()
        else:
            viewspec = self.view
        
        q = self.buildTable(viewspec)
        out = (
            f"<table>\n"
            f"{toHeaderStr(q["colHeader"])}\n"
            f"{toDataStr(q["dataBlock"])}\n"
            f"</table>\n"
        )
        return out



    def buildTable(self, viewspec):
        #print(viewspec)

        def buildTableHeader():
            
            return "Dimension Header"

        def buildColHeader():
            out = viewspec["cols"]
            return out

        def buildDataBlock():
            
            rows = self.q.enumerateAddresses()
            cols = viewspec["cols"]
            rows = [buildRow(row, cols) for row in rows]
            
            return rows
        
        
        
        def buildRow(query, cols):
            cells = []
            for col in cols:
                if col in query:
                    cells.append(query[col])
                else: #you are in a value
                    cells.append(self.q.getValue(query))
            
            return cells
        
        
        table = {
            "tableHeader" : buildTableHeader(),
            "colHeader": buildColHeader(),
            "dataBlock": buildDataBlock()
        }

        return table




class Qube:
    
    def __init__(self, dimensions, measures) -> None:
        self.q = mdq()
        self.q.setDims(dimensions, measures)
        self.view = QubeViewer(self.q)
        

    def __str__(self) -> str:
        return self.view.toString()
    
    # def __repr__(self) -> str:
    #     return self.__str__()
    
    def _repr_html_(self) -> str:
        return self.view.toHTML()
    
    def setValue(self, dims_addr: dict, value) -> None:
        self.q.setValue(dims_addr, value)

    def getValue(self, dims_addr: dict):
        return self.q.getValue(dims_addr)

    def setView(self, rows, cols):
        self.view.setView(rows,cols)

        





    















 




