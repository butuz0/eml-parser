#!/usr/bin/env bash
set -euo pipefail

if [ -z "${1:-}" ]; then
  echo "Error: Target directory not specified." >&2
  echo "Usage: $0 <target_directory>" >&2
  exit 1
fi

if [ ! -d "$1" ]; then
  echo "Error: Directory '$1' does not exist." >&2
  exit 1
fi

TARGET_DIR="${1%/}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="${TARGET_DIR}/output_${TIMESTAMP}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="python3"
PARSE_SCRIPT="${PROJECT_ROOT}/main.py"

total_found=0
success_count=0
error_count=0

parse_eml_files(){
  mkdir "$OUTPUT_DIR"

  echo "Scanning for .eml files in: ${TARGET_DIR}..."

  while IFS= read -r -d '' file; do
    ((total_found++))

    local filename
    filename=$(basename "$file" .eml)

    if "$PYTHON" "$PARSE_SCRIPT" "$file" "${OUTPUT_DIR}/${filename}"; then
      ((success_count++))
    else
      ((error_count++))
    fi
  done < <(find "$TARGET_DIR" -type f -name "*.eml" -print0)
}

print_statistics() {
  local parsed_attachments=0

  if [ -d "$OUTPUT_DIR" ]; then
    parsed_attachments=$(find "$OUTPUT_DIR" \
      -type f \
      -not \( -name "body.txt" \
      -or -name "body.html" \
      -or -name "meta.json" \) \
      | wc -l)
  fi

  echo -e "\n=========================================="
  echo "Total .eml files found:  ${total_found}"
  echo "Successfully processed:  ${success_count}"
  echo "Failed with errors:      ${error_count}"
  echo "Total attachments saved: ${parsed_attachments}"
  echo -e "==========================================\n"
}

archive_output(){
  if [ "$success_count" -gt 0 ]; then
    local archive_name="${TARGET_DIR}_${TIMESTAMP}.tgz"

    tar -czf "${archive_name}" -C "${TARGET_DIR}" "output_${TIMESTAMP}"
    rm -rf "$OUTPUT_DIR"

    echo "Output archived to ${archive_name}"
  else
    echo "No files were successfully parsed. Skipping archive creation."
    rmdir "$OUTPUT_DIR"
  fi
}

main() {
  parse_eml_files
  print_statistics
  archive_output
}

main "$@"