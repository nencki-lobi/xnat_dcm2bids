### Summary Table

| Problem Description                    | Recommended Action                         | Files/Paths Involved                    |
| -------------------------------------- | ------------------------------------------ | --------------------------------------- |
| Missing files in `bids` directory      | Check `tmp_dcm2bids` for unprocessed files | `tmp_dcm2bids`                          |
| Files in `tmp_dcm2bids` not converted  | Review and modify `config.json`            | `tmp_dcm2bids`, `config.json`           |
| Incomplete or broken downloaded data   | Delete session data to re-download         | `{sourcedata}/{xnat_session_id}`        |
| Need to overwrite previous BIDS output | Remove temporary and subject-specific dirs | `tmp_dcm2bids`, `bids/sub-{subject_id}` |

---
### Scenarios

**Problem:** Some files are missing in your `bids` directory.

**Solution:**
  Check the `tmp_dcm2bids` directory for unprocessed files.

---

**Problem:** Files remain in `tmp_dcm2bids` but are not converted to the BIDS structure.

**Solution:**
  Inspect your `config.json` file. It may need modifications to correctly map and convert these files.

---

**Problem:** The downloaded data is incomplete or corrupted but exists in XNAT.

**Solution:**
  Delete the following directory to re-download the XNAT data:

  ```bash
  {sourcedata}/{xnat_session_id}
  ```

---

**Problem:** You want to overwrite previous output in the BIDS directory.

**Solution:**
  Remove the following directories before re-running the process:

  ```bash
  tmp_dcm2bids
  bids/sub-{subject_id}
  ```

---
### Links
- [dcm2bids](https://unfmontreal.github.io/Dcm2Bids/)
- [xnatutils](https://github.com/Australian-Imaging-Service/xnatutils)