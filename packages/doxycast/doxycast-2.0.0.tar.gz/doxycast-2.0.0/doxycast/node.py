import textwrap

class node:
    parent                      = None
    children                    = list()
    doxygen_id                  = str()
    type                        = str()
    name                        = str()
    definition                  = str()
    brief                       = str()
    details                     = str()

    def __init__(self, **kwargs):
        """
        Initializes a node.
        """
        for key in kwargs:
            exec(textwrap.dedent(f"""
                self.{key} = kwargs["{key}"]
            """))

    def __eq__(self, other) -> bool:
        """
        Checks if a node equals to another.
        """
        try:
            return self.doxygen_id == other.doxygen_id
        except:
            return False

    def reparent(self, new_parent) -> None:
        """
        Reparents the node.
        """
        try:
            if self.parent != None:
                self.parent.children.remove(self)
        except ValueError:
            pass

        new_parent.children.append(self)
        self.parent = new_parent

    def child(self, doxygen_id: str):
        """
        Returns the child (or grandchild) with given ``doxygen_id``.
        """
        for child_node in self.children:
            if child_node.doxygen_id == doxygen_id:
                return child_node

            try:
                return child_node.child(doxygen_id)
            except IndexError:
                pass

        raise IndexError(f"doxycast.node.node.child: invalid id given: \"{doxygen_id}\"")

class graph_node:
    label       = str()
    refid       = int()
    children    = list()

    def __init__(self, label, refid, children=list()):
        """
        Initializes a graph node.
        """
        self.label      = label
        self.refid      = refid
        self.children   = children
