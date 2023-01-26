"""
What is functional dependency?

    - Functional dependency is a concept in database design and normalization.
    - It refers to the relationship between two attributes (or columns) in a table, where the value of one attribute is determined by the value of another attribute.
    - In other words, if the value of attribute A is known, the value of attribute B can be determined.
    - In database design, functional dependencies are used to identify and eliminate redundancy in the data, and to ensure data integrity and consistency.


What is canonical or minimal cover of functional dependency?

    - A canonical or minimal cover of functional dependencies (FDs) is a set of FDs that includes all the dependencies that are logically implied by the original set of FDs, but no redundant dependencies.
    - In other words, it is a minimal set of FDs that still implies all the dependencies of the original set.

    - A set of FDs is considered to be in canonical cover if and only if it satisfies the following properties:

        1. It contains no extraneous attributes.
        2. It contains no redundant dependencies.
        3. It is in minimal form.

    - For example, if A->B and B->C are given functional dependencies, the canonical cover will be A->B,B->C and not A->B,B->C,A->C as A->C is redundant.

    It is important to find the canonical cover of a set of functional dependencies because it can be used to find the minimal set of attributes required to determine all other attributes in a table, which can simplify the design and improve the performance of the database.

Steps to find minimal cover of functional dependecies.

    1. Apply the rules of functional dependency to the given set of FDs to ensure that each FD has only one attribute on the right-hand side.
    2. Remove any FDs that contain attributes not belonging to the relation.
    3. Remove any extraneous attributes from the left-hand side of the FDs.
    4. Eliminate any redundant FDs from the set.
"""

from copy import deepcopy


class FDSet:
    """
    Class representing a functional dependency set.

    TODO:
        1. Currently only creating the FD Set for the alphabet characters. For example, {A->B, C->D}.
        It doesn't works with the real attribute like {rollno->name, rollno->age}
        2. A good way to create relation of the FD.
    """

    def __init__(self, num_of_fds: int, relation: tuple = None):
        """
        Initialize the FDSet object with the number of functional dependencies and the relation.

        Args:
            num_of_fds (int): The number of functional dependencies in the set.
            relation (tuple, optional): A tuple representing the relation. Defaults to None.
        """

        # No. of FDs in the set
        self.num_of_fds = num_of_fds

        # Set to store the fds
        self.fd_set = set()

        # If user has passed relation, used that, else create a new relation
        if relation:
            self.R = relation
        else:
            self.R = FDSet.create_relation()

    @property
    def _fd_set(self):
        """
        Get the functional dependency set.

        Returns:
            set: The functional dependency set.
        """
        return self.fd_set

    @_fd_set.setter
    def _fd_set(self, fd_set):
        self.fd_set = fd_set

    @staticmethod
    def create_relation():
        """
        Create a new relation by asking the user for the number of attributes and their values.

        Returns:
            tuple: A tuple representing the relation.
        """
        R = []
        print("Before creating functional dependency, you must defined the relation.")

        # Total attributes of the relation
        num_attrs = int(input("Enter number of attributes you want in the relation: "))

        # Add the attribute in the relation
        for idx in range(1, num_attrs + 1):
            R.append(input(f"Enter attribute {idx} value: "))

        # Convert relation list to tuple
        return tuple(R)

    @staticmethod
    def closure_of_attr(fd_set, attr):
        """
        closure_of_attr is a function that finds the closure of a given set of attributes in a functional dependency set. It uses the concept of attribute closure, where the closure of a set of attributes is the set of attributes that can be inferred from the given set of attributes.

        Args:
            fd_set: the functional dependency set
            attr: the set of attributes for which the closure is to be found

        Returns: the closure of the given set of attributes
        """
        closure = {attr}
        for _ in range(len(fd_set)):
            for fd in fd_set:
                if set(fd[0]).issubset(closure):
                    closure.add(fd[1])
        return closure

    def create_fd_set(self):
        """
        Create a new functional dependency set by asking the user for the left-hand side and right-hand side of each functional dependency.
        """
        for num in range(1, self.num_of_fds + 1):
            # LHS of the functional dependency
            fd_lhs = input(f"Enter LHS of FD {num}: ").upper()
            # RHS of the functional dependency
            fd_rhs = input(f"Enter RHS of FD {num}: ").upper()

            # Check for the trivial dependency
            if fd_lhs == fd_rhs:
                self.fd_set = []
                print(
                    "You can not add the trivial functional dependency! Better luck next time!"
                )
                return
            self.fd_set.add((fd_lhs, fd_rhs))

    @staticmethod
    def print_fd_set(fd_set):
        """
        Print the functional dependency set.

        Args:
            fd_set (set): A set of functional dependencies.
        """
        fd_set_str_set = set()
        for fd in fd_set:
            fd_set_str_set.add(f"{fd[0]} -> {fd[1]}")
        print(f"Functional Dependency set: {fd_set_str_set}")

    def __str__(self) -> str:
        """
        Get a string representation of the functional dependency set.

        Returns:
            str: A string representation of the functional dependency set.
        """
        print(f"Functional Dependencies: {self.fd_set}")


class MinimalCover:
    """
    This class MinimalCover is used to find the minimal cover of a given functional dependency set.

    Methods:
    simplify_fd_set(): Simplify the given fd set
    remove_fd_not_present_in_relation(): Remove the fd whose attributes does not belongs to R

    TODO:
        1. Currently working only with alphabet characters i.e. A, B, C, D, ..
        2. It only works correctly if only one alphabet character is present at the LHS.
    """

    def __init__(self, fd_set, relation) -> None:
        """
        The constructor of the MinimalCover class.

        This function is used to initialize the attributes of the MinimalCover class with the given functional dependency set and relation.

        Args:
        fd_set (set): set of functional dependencies
        relation (tuple): Tuple of attributes
        """
        self.fd_set = fd_set
        self.R = relation
        self.is_simplified = False
        self.is_attr_not_belongs_to_R_removed = False
        self.is_redundent_fd_removed = False
        self.result = []

    def simplify_fd_set(self):
        """
        Simplify the given functional dependency set

        This function is used to simplify the given functional dependency set by breaking the RHS of a FD into single attributes.

        Returns:
        set: simplified functional dependency set
        """

        if self.is_simplified:
            return self.fd_set

        self.simplified_fd_set = set()
        for fd in self.fd_set:
            if len(fd[1]) > 1:
                for char in fd[1]:
                    self.simplified_fd_set.add((fd[0], char))
            else:
                self.simplified_fd_set.add((fd[0], fd[1]))
        self.is_simplified = True
        return self.simplified_fd_set

    def remove_fd_not_present_in_relation(self):
        """
        Remove functional dependencies whose attributes not present in relation

        This function is used to remove the functional dependencies whose attributes are not present in the relation.

        Returns:
        set: functional dependency set after removing fd with attributes not in R
        """
        # Check if fds that doesn't belongs to relation are already removed.
        if self.is_attr_not_belongs_to_R_removed:
            return self.fd_set

        # If FD set is not simplfied then simply it.
        if not self.is_simplified:
            self.fd_set = self.simplify_fd_set()

        # Create a deepcopy of the fd set.
        fd_set = deepcopy(self.fd_set)
        fd_set_deepcopy = deepcopy(fd_set)
        for fd in fd_set_deepcopy:
            # If LHS or RHS of FD is doesn't belongs to relation R then remove the FD.
            if (fd[0] not in self.R) or (fd[1] not in self.R):
                fd_set.remove(fd)

        self.remove_fd_whose_attr_not_in_R = fd_set
        # The FD set successfully removed the FDs that doesn't belongs to R, so mark flag as True
        self.is_attr_not_belongs_to_R_removed = True
        return self.remove_fd_whose_attr_not_in_R

    def remove_redundent_fd(self):
        """
        The method that removes any functional dependencies that are redundant from the functional dependency set. It uses the concept of attribute closure to check if a functional dependency can be inferred from the remaining functional dependencies and removes it if it can.

        Returns:
            the functional dependency set with any redundant functional dependencies removed
        """
        # Check if redundent FDs are already removed
        if self.is_redundent_fd_removed:
            return self.fd_set

        # Check if FDs doesn't belongs to R are removed or not.
        if not self.is_attr_not_belongs_to_R_removed:
            self.fd_set = self.remove_fd_not_present_in_relation()

        # Create a deepcopy of the fd set.
        fd_set = deepcopy(self.fd_set)
        fd_set_deepcopy = deepcopy(fd_set)
        for fd in fd_set_deepcopy:

            # To track the original fd set state, create temp fd set
            temp_fd_set = deepcopy(fd_set)

            # Remove the current fd
            temp_fd_set.remove(fd)

            # Current fd LHS and RHS
            fd_lhs, fd_rhs = fd[0], fd[1]

            # Find closure of LHS of current FD from temp_fd_set
            closure_of_fd_lhs = FDSet.closure_of_attr(temp_fd_set, fd_lhs)

            # If RHS can be find in the FD's LHS closure even after
            # removing the current FD from FD set then the current FD is redundent FD.
            if fd_rhs in closure_of_fd_lhs:
                fd_set = temp_fd_set

        self.removed_redundent_fd = fd_set
        # The redundent FDs are removed, mark the flag as True
        self.is_redundent_fd_removed = True
        return self.removed_redundent_fd

    def canonical_cover(self):
        """
        The method returns the canonical cover of the functional dependency set. It first simplifies the functional dependency set by removing any extraneous attributes, then removes any functional dependencies that are not present in the relation, and finally removes any redundant functional dependencies.

        Returns: the canonical cover of the functional dependency set
        """
        # Simplify the FD set.
        self.fd_set = self.simplify_fd_set()

        # Remove the FDs that doesn't belongs to relation from the FD set.
        self.fd_set = self.remove_fd_not_present_in_relation()

        # Remove any redundent FDs.
        self.fd_set = self.remove_redundent_fd()

        # Return canonical cover i.e. minimal cover of the FD set.
        return self.fd_set


if __name__ == "__main__":

    num_of_fds = 5
    fd_set_obj = FDSet(num_of_fds, relation=("A", "B", "C", "D", "E"))
    fd_set_obj._fd_set = {("A", "BE"), ("A", "C"), ("C", "B"), ("D", "F"), ("C", "R")}
    fd_set = fd_set_obj._fd_set
    print("***** FUNCTIONAL DEPENDENCIES *****")
    FDSet.print_fd_set(fd_set)

    mc = MinimalCover(fd_set, fd_set_obj.R)
    new_fd_set = mc.canonical_cover()
    print("\n***** CANONICAL COVER OF FUNCTIONAL DEPENDENCY *****")
    FDSet.print_fd_set(new_fd_set)
