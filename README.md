# Important considerations
* Attention to requirement details counts
* No commented code
* No unnecessary changes(like changing `README.md`)
* Each PR should be created against current `stepX`

# Step 1
Please suggest a PR with
1. a python script implementing the below contract
2. a test verifying standard output produced by the script is correct
  * make sure to create a test in a `tests` folder

*hint: the test should call the script, catching std output and verifying its correctness by asserting against some constant expected value*

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
