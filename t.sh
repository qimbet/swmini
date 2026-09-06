count=0
testLine="python -m src.game.startup"

> errs.txt

for i in {1..100}; do
    output=$($testLine 2>&1)

    if [[ "$output" == *"RuntimeError"* ]]; then
        ((count++))

        {
            echo "========================================"
            echo "Run $i"
            echo "========================================"
            echo "$output"
            echo
        } >> errs.txt
    fi
done

echo "RuntimeError found: $count / 100"
echo "Errors saved to errs.txt"
