from core.formula import *
from core.cnf import *
from utils.parser import *
from revision.belief_base import *
from entailment.resolution import *
from revision.contraction import *
from revision.expansion import *
from revision.revision import *

from tests.test_revision import *
from tests.test_contraction import *

if __name__ == "__main__":
    print("Enter the formula you would like to enter the belief base:")
    print("\tYou can assign a priority to the formula, by typing 'formula, priority', where priority is an integer")
    print("Press ctrl + c to exit program.")

    belief_base = BeliefBase()

    # revision_success_consistency_test()
    # revision_vacuity_test()
    # revision_inclusion_test()
    # revision_extensionality_test()

    # contraction_test_vacuity()
    # contraction_test_success()
    # contraction_test_priority()
    # contraction_test_extensionality()
    # contraction_test_recovery()

    while True:
        try:
            user_input = input("> ")

            if user_input.startswith("1"):
                revision_success_consistency_test()
            elif user_input.startswith("2"):
                revision_vacuity_test()
            elif user_input.startswith("3"):
                revision_inclusion_test()
            elif user_input.startswith("4"):
                revision_extensionality_test()
            elif user_input.startswith("5"):
                contraction_test_vacuity()
            elif user_input.startswith("6"):
                contraction_test_success()
            elif user_input.startswith("7"):
                contraction_test_priority()
            elif user_input.startswith("8"):
                contraction_test_extensionality()
            # elif user_input.startswith("9"):
            #     contraction_test_recovery()
            else:
                user_input = user_input.strip().split(",")
                formula = parse_formula(user_input[0].strip())
                priority = int(user_input[1].strip()) if len(user_input) == 2 else 0
                
                if entails(belief_base, formula):
                    belief_base = expand(belief_base, formula, priority=priority)
                else:
                    belief_base = revise(belief_base, formula, priority=priority)

                print(f"The belief base has been updated to: {belief_base.pretty_print_belief_base()}")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
