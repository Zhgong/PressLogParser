import re
import logging
import pandas as pd
from typing import List, Dict, Any, Tuple


def _parse_header_metadata(lines: List[str]) -> Dict[str, str]:
    """Parse metadata from the first four lines if they are in header format."""
    if len(lines) < 2:
        return {}

    # Detect the pattern [Field];[Field];... in the first line
    if not re.match(r"\[[^\]]+\];", lines[0]):
        return {}

    metadata: Dict[str, str] = {}

    def parse_pair_line(header_line: str, value_line: str) -> None:
        headers = [h.strip()[1:-1] for h in header_line.split(";") if h]
        values = [v.strip() for v in value_line.split(";")]
        for key, val in zip(headers, values):
            if key:
                key_norm = re.sub(r"[^a-z0-9_]+", "", key.lower().replace(" ", "_"))
                if val:
                    metadata[key_norm] = val

    parse_pair_line(lines[0], lines[1])
    if len(lines) >= 4:
        parse_pair_line(lines[2], lines[3])

    return metadata

logger = logging.getLogger(__name__)

class LogParser:
    def __init__(self, file_content: str) -> None:
        self.file_content: str = file_content

    def parse_log(self) -> Tuple[Dict[str, str], List[pd.DataFrame]]:
        metadata: Dict[str, str] = {}
        records: List[Dict[str, Any]] = []
        record_section: bool = False
        current_record: Dict[str, Any] = {}

        lines = self.file_content.splitlines()

        # Attempt to parse metadata contained in the first four lines
        header_meta = _parse_header_metadata(lines[:4])
        if header_meta:
            metadata.update(header_meta)
            start_index = 4
        else:
            start_index = 0

        for line in lines[start_index:]:
            if "[Recorded curves]" in line:
                record_section = True

            elif "[Variables]" in line:  # End of recorded curves section
                record_section = False


            # Extract records within "[Recorded curves]"
            if record_section:
                if line.startswith("[Record "):
                    # Start a new record
                    current_record = {"points": []}
                    records.append(current_record)
                elif re.match(r"^\d+;\d+\.\d+;-?\d+\.\d+(?:[eE][-+]?\d+)?;T#.*$", line):
                    # Parse points within the current record
                    fields: List[str] = line.split(";")
                    point: int = int(fields[0])
                    position: float = float(fields[1])
                    force: float = float(fields[2])
                    time: str = fields[3]
                    time_ms = parse_time(time)  # Use the shared function to parse time
                    current_record["points"].append({"Point": point, "Position": position, "Force": force, "Time (ms)": time_ms})
                else:
                    logger.warning("Invalid line skipped: %s", line)
            else:
                key_val = re.match(r"([^;:]+)[;:]\s*(.+)", line)
                if key_val:
                    key = key_val.group(1).strip().lower().replace(" ", "_")
                    value = key_val.group(2).strip()
                    metadata[key] = value
                    continue

                result_match = re.match(
                    r"(window|threshold|envelope).*?:\s*(.+)",
                    line,
                    re.IGNORECASE,
                )
                if result_match:
                    result_key = f"{result_match.group(1).lower()}_result"
                    metadata[result_key] = result_match.group(2).strip()

        # Convert records into a list of dataframes
        record_dfs: List[pd.DataFrame] = [pd.DataFrame(record["points"]) for record in records if "points" in record]
     
        record_dfs = [df for df in record_dfs if not df.empty]
       
        for df in record_dfs:
            df['Time (ms)'] = df['Time (ms)'] - df['Time (ms)'][0]
        return metadata, record_dfs

def parse_time(time_str: str) -> int:
    match = re.match(r'T#(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?(\d+)ms', time_str)
    if not match:
        match = re.match(r'T#(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', time_str)
    if match:
        days = int(match.group(1)) if match.lastindex >= 1 and match.group(1) else 0
        hours = int(match.group(2)) if match.lastindex >= 2 and match.group(2) else 0
        minutes = int(match.group(3)) if match.lastindex >= 3 and match.group(3) else 0
        seconds = int(match.group(4)) if match.lastindex >= 4 and match.group(4) else 0
        milliseconds = int(match.group(5)) if match.lastindex == 5 and match.group(5) else 0
        return (days * 24 * 60 * 60 * 1000) + (hours * 60 * 60 * 1000) + (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
    return 0
