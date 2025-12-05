#!/bin/bash

echo "Running Smoke Test..."

# ---------- CHECK APPLICATION ----------
if curl -is --max-redirs 10 http://localhost:8080 -L | grep -w "HTTP/1.1 200" > /dev/null; then
    echo "================="
    echo "Smoke Test passed"
    echo "================="
else
    echo "============================================================="
    echo "Unable to reach application on port 8080 !!"
    echo "============================================================="
fi


# ---------- CHECK TRIVY RESULTS ----------
if grep -q "CRITICAL" trivyresults.txt; then
    echo "============================================================="
    echo "Docker Image praveenkumar446/democicd:latest has CRITICAL vulnerabilities!!"
    echo "============================================================="
else
    echo "============================================================="
    echo "Docker Image praveenkumar446/democicd:latest is safe (no CRITICAL vulns)"
    echo "============================================================="
fi

exit 0
