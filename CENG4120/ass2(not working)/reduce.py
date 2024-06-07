POS = 1        # Positive
NEG = 0        # Negative
DONTCARE = 2   # Don't care

def parse_input_function(input_file):
    no_of_variables = int(next(input_file).strip())
    no_of_cubes = int(next(input_file).strip())
    f = []
    for _ in range(no_of_cubes):
        line = next(input_file).strip()
        cube = [DONTCARE if x == '2' else int(x) for x in line]
        f.append(cube)
    return no_of_variables, f

def has_all_dc_cube(f):
    """Check if there is an all-DC cube in the function."""
    return any(all(x == DONTCARE for x in cube) for cube in f)

def is_unate(f):
    """Check if a Boolean function is unate."""
    if not f:
        return False
    
    for i in range(len(f[0])):
        seen = set()
        for cube in f:
            if cube[i] != DONTCARE:
                if cube[i] in seen:
                    return False
                seen.add(cube[i])
    return True

def is_binate(f, var_index):
    """Check if a variable is binate in the function."""
    polarities = {cube[var_index] for cube in f if cube[var_index] != DONTCARE}
    return len(polarities) == 2

def find_most_binate_variable(f, m):
    """Find the most binate variable."""
    binate_counts = [(var_index, sum(1 for cube in f if cube[var_index] != DONTCARE)) for var_index in range(m)]
    binate_counts = sorted(binate_counts, key=lambda x: -x[1])
    for var_index, _ in binate_counts:
        if is_binate(f, var_index):
            return var_index
    return None

def branch(f, var_index, polarity):
    """Branch on a variable with the given polarity."""
    new_f = []
    for cube in f:
        if cube[var_index] == polarity or cube[var_index] == DONTCARE:
            new_cube = cube.copy()
            new_cube[var_index] = DONTCARE
            new_f.append(new_cube)

    # print(f"Branching on variable {var_index} with polarity {polarity}. Resulting cubes:")
    # for cube in new_f:
    #     print(''.join(str(x) for x in cube))
    return new_f

def tautology_check(f, m):
    if has_all_dc_cube(f):
        return True
    if is_unate(f) and not has_all_dc_cube(f):
        return False
    var_to_split = find_most_binate_variable(f, m)
    if var_to_split is None:
        return False
    
    # print("Starting tautology check for the following cubes:")
    # for cube in f:
    #     print(''.join(str(x) for x in cube))

    f_positive = branch(f, var_to_split, POS)
    f_negative = branch(f, var_to_split, NEG)
    return (tautology_check(f_positive, m) and tautology_check(f_negative, m))


def write_output_file(output_file_path, m, cubes):
    with open(output_file_path, 'w') as file:
        file.write(f"{m}\n{len(cubes)}\n")
        for cube in cubes:
            # Convert each cube back to string representation
            cube_str = ''.join(str(DONTCARE) if x == DONTCARE else str(x) for x in cube)
            file.write(f"{cube_str}\n")


    

  
   





def redundant_cube_removal(F, m):
    E = set()  # Initialize set of relatively essential cubes
    R = set()  # Initialize set of totally redundant cubes
    
    # Stage 1: Identify relatively essential cubes E

    for cube in F:
        F_without_Cofactor = [c for c in F if c != cube]
        F_without_Cofactor_of_C = []

        # Compare each cube in F_without_Cofactor with the current cube
        for other_cube in F_without_Cofactor:
            modified_cube = list(other_cube)
            det = True
            for j, bit in enumerate(other_cube):
                if other_cube[j] == 2:
                    continue
                if other_cube[j] == cube[j] and cube[j] != 2:
                    modified_cube[j] = 2
                if other_cube[j] != cube[j] and cube[j] != 2:
                    det = False
            if det:
                F_without_Cofactor_of_C.append(modified_cube)
            
        if not tautology_check(F_without_Cofactor_of_C, m):
            E.add(tuple(cube))
    
    # Stage 2: Identify totally redundant cubes R
    F_without_E = [tuple(c) for c in F if tuple(c) not in E]
    F_without_Cofactor_of_E = []
    for Rcube in F_without_E:
        for Ecube in E:
            modified_cube = list(Ecube)
            det = True
            for j, bit in enumerate(Ecube):
                if Ecube[j] == 2:
                    continue
                if Ecube[j] == Rcube[j] and Rcube[j] != 2:
                    modified_cube[j] = 2
                if Ecube[j] != Rcube[j] and Rcube[j] != 2:
                    det = False
            if det:
                F_without_Cofactor_of_E.append(modified_cube)

        if not tautology_check(F_without_Cofactor_of_E, m):
            R.add(tuple(Rcube))
                

    # Final result: F without the redundant cubes R
    reduced_F = [list(cube) for cube in F if tuple(cube) not in R]
    print (R)
    return reduced_F


    




#              E= [[0,1,2],[2,0,2]]
#              F\E = [[1, 0, 2], [0, 0, 2]]
#              C1 = [1, 0, 2]
#              C2 = [0, 0, 2]
#              "F not C cofactor of C": [2,0,2] >[2,2,2]
#            
#         algo:
#             "F": [[1, 0, 2], [0, 1, 2], [0, 0, 2],[2,0,2]],

#             "F not C": [[0,1,2] [0,0,2],[2,0,2]],
#             "C" : [1,0,2],               
#             "F not C cofactor of C": [2,0,2] >[2,2,2]
#             tautology_check([2,2,2])
#             if return true # not essentail


#             "F not C": [1,0,2] [0,0,2],[2,0,2]
#             "C": [0,1,2]
#             "F not C cofactor of c": []
#             tautology_check([])
#             if return false #essentail

#             "F not C": [1,0,2] [0,1,2],[2,0,2]
#             "C": [0,0,2]
#             "F not C cofactor of c": [2,2,2]
#             tautology_check([2,2,2])
#             if return true #not essentail

#             "F not C": [1,0,2] [0,1,2],[0,0,2]
#             "C": [2,0,2]
#             "F not C cofactor of c": [[1,2,2],[0,2,2]]
#             tautology_check([[1,2,2],[0,2,2]])
#             if return true #not essentail

#             E=[[0,1,2]]
#         },
#         ]    
  

def test1():
    F=[[1, 0, 2], [0, 1, 2], [0, 0, 2], [2, 0, 2]]
    redundant_cube_removal(F, 3)  


def test_tautology_check():
    test_cases = [
        # Not a tautology: Different outcomes based on input
        ([[1, 2, 0], [0, 2, 1]], False),
        # Is a tautology: Covers all possible input combinations
        ([[1, 2, 2], [2, 2, 2]], True),
        # Not a tautology: Missing combinations for a tautology
        ([[1, 1, 1]], False),
        # Is a tautology: Every possible combination is covered by DC
        ([[2, 2, 2]], True),
        # More complex case, should evaluate the logic carefully
        ([[1, 0, 1], [0, 1, 0], [2, 2, 2]], True),
        # Not a tautology: Partial coverage only
        ([[1, 0, 2], [0, 1, 2]], False),
    ]

    for f, expected in test_cases:
        m = len(f[0])
        result = tautology_check(f, m)
        assert result == expected, f"Failed on {f}. Expected {expected}, got {result}"
    print("All tautology check tests passed.")

def main(input_file_path, output_file_path):
    test_tautology_check()
    test1()
    with open(input_file_path, 'r') as input_file:
        m, f = parse_input_function(input_file)
    
    # Assuming the tautology check does not directly influence cube filtering for redundancy.
    # result = tautology_check(f, m)  # The tautology check result might not be needed for filtering.
    
    filtered_cubes = redundant_cube_removal(f,m)  # Apply redundancy filtering logic here.
    write_output_file(output_file_path, m, filtered_cubes)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)
    
    in_file, out_file = sys.argv[1], sys.argv[2]
    main(in_file, out_file)
