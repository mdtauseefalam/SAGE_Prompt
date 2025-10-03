import os

def construct_prompt(sol_file, cfg_file, cg_file, dd_file, example_files, output_file):

    def read_file(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    # Read inputs
    sol_code = read_file(sol_file)
    cfg = read_file(cfg_file)
    cg = read_file(cg_file)
    dd = read_file(dd_file)

    # Base prompt
    prompt = """You are an excellent smart contract vulnerability detector. 
                Analyze the smart contract provided after [Solidity Code], written in Solidity.
                Additional semantic context is included via its Control Flow Graph [CFG], Call Graph
                [CG], and Data Dependency [DD]. Reference examples of similar vulnerabilities are
                given under [<Vulnerability Type> Example] to support your reasoning. Determine:
                (a) Is the contract vulnerable? (Yes or No) and (b) If yes, specify the vulnerability type (e.g.,
                Reentrancy, Arithmetic, etc.)

                Your Answer: {Vulnerability: ⟨Yes/No⟩, Vulnerability Type: ⟨Reentrancy/Arithmetic/...⟩}  """

    # Insert contents
    prompt += f"[Solidity Code]\n{sol_code}\n\n"
    prompt += f"[CFG]\n{cfg}\n\n"
    prompt += f"[CG]\n{cg}\n\n"
    prompt += f"[DD]\n{dd}\n\n"

    # Add vulnerability examples
    for vuln_type, file_path in example_files.items():
        vuln_example = read_file(file_path)
        prompt += f"[{vuln_type} Example]\n{vuln_example}\n\n"

    # Save to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"Prompt constructed and saved to {output_file}")


# Example usage:
if __name__ == "__main__":
    sol_file = "/content/reentrancy_dao.sol"
    cfg_file = "/content/reentrancy_dao_CFGs.txt"
    cg_file = "/content/reentrancy_dao_CG.txt"
    dd_file = "/content/reentrancy_dao_DD_Encoded.txt"
    example_files = {
        "Reentrancy": "/content/reentrancy.txt",
        "Arithmetic": "/content/arithmetic.txt"
    }
    output_file = "final_prompt.txt"

    construct_prompt(sol_file, cfg_file, cg_file, dd_file, example_files, output_file)
