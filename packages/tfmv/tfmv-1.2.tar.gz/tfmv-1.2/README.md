# tfmv

Simple tool for moving / renaming resources in one or several terraform configurations.

---

When moving or renaming resources or modules in terraform configurations, objects in the corresponding state
are typically destroyed and recreated by `terraform apply`.

This may be impractical, or impossible for certain resources, and the objects in the state must be moved manually,
one by one, to prevent this.

This tool helps to automate this state operation.



The operations are:
- `terraform state pull` to get local copies of the remote state(s)
- `terraform state list` to identify objects matching the given prefix
- `terraform state mv` is called to move or rename the resource based on the prefix
- `terraform state push` to push the modified state back to the remote 
- clean *local files*


### Usage:

- **rename:**
    ```bash
    tfmv google_compute_network.old_name google_compute_network.new_name --src /home/vincent/my-project 
    ```

- **move from root to module:**
    ```bash
    tfmv google_compute_network.vpc module.my_module.google_compute_network.vpc --src /home/vincent/my-project  
    ```

- **renaming module:**
    ```bash
    tfmv module.my_module module.my_module_renamed --src /home/vincent/my-project  
    ```
