# Step 1
Please suggest a PR with a python code implementing the below contract. Remember to implement a test verifying the output is correct also.

# Python dead links

## Input arguments
The program expects target url to take HTML(and check for dead links) from.

Example command line:
`python <your_python_script> <url>`

## Output format

```
{
    "url": "<input_url_tocheck>"
    "404":  {
        "size": 3,
	"urls": ["url1", "url2", "url3"]
    },
    "50x": {
        "size": 1,
	"urls" ["url4", ]
    }
    "dead": 4,
    "total": 10
}
```

It is ok to use YML/XML or any other format (not only JSON) considering the test verifying this format is available.

*N.B.: it worth to think of various edge cases related to CLI usage, potential connection and/or content issues and cover them in your code*
