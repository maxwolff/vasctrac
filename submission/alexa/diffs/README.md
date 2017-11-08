## Run from ~/humana

Ensure the versions match and that the header line paths
have been appropriately updated.


### alexa-sdk v1.0.9
Note save state in v1.0.10 seems broken during test flow
```sh
$ patch -p4 < diffs/alexa-sdk/alexa.js_v1_0_9.diff
```

### aws-lambda-mock-context v3.1.1
```sh
$ patch -p4 < diffs/aws-lambda-mock-context/index.js.diff
```

### gulp-jshint v2.0.4
```sh
$ patch -p4 < diffs/gulp-jshint/lint.js.diff
```

### jshint v2.9.4
```sh
$ patch -p4 < diffs/jshint/jshint.js.diff
```
```sh
$ patch -p4 < diffs/jshint/options.js.diff
```

### jshint-stylish v2.2.1
```sh
$ patch -p4 < diffs/jshint-stylish/index.js.diff
```