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
PARENT_DIR=$(dirname "$TARGET_DIR")
BASE_NAME=$(basename "$TARGET_DIR")
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

OUTPUT_NAME="${BASE_NAME}_output_${TIMESTAMP}"
OUTPUT_DIR="${PARENT_DIR}/${OUTPUT_NAME}"
ARCHIVE_PATH="${PARENT_DIR}/${OUTPUT_NAME}.tgz"
LOG_FILE="${PARENT_DIR}/${OUTPUT_NAME}.log"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="python3"
PARSE_SCRIPT="${PROJECT_ROOT}/main.py"

PARSED_TEXT="body.txt"
PARSED_HTML="body.html"
PARSED_META="meta.json"

total_found=0
success_count=0
error_count=0

log_info() {
  echo "[$(date '+%Y-%m-%d %T')] INFO: $*"
}

log_error() {
  echo "[$(date '+%Y-%m-%d %T')] ERROR: $*" >&2
}

parse_eml_files(){
  mkdir "$OUTPUT_DIR"

  log_info "Scanning for .eml files in: ${TARGET_DIR}..."

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
    parsed_attachments=$(( $(find "$OUTPUT_DIR" \
      -type f \
      -not \( -name "$PARSED_TEXT" \
      -or -name "$PARSED_HTML" \
      -or -name "$PARSED_META" \) \
      | wc -l) ))
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
    tar -czf "$ARCHIVE_PATH" -C "$PARENT_DIR" "$OUTPUT_NAME"
    rm -rf "$OUTPUT_DIR"

    log_info "Output archived to ${ARCHIVE_PATH}"
  else
    log_error "No files were successfully parsed. Skipping archive creation."
    rmdir "$OUTPUT_DIR"
  fi
}

run_pipeline(){
  parse_eml_files
  print_statistics
  archive_output
}

main() {
  run_pipeline 2>&1 | tee "$LOG_FILE"
}

main "$@"