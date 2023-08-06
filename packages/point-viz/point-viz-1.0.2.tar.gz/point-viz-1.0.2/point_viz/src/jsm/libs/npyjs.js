// this is the code from https://github.com/aplbrain/npyjs.git
// it has been modified to fit the usage of this application
function npyjs() {

    this.dtypes = {
        "<u1": {
            name: "uint8",
            size: 8,
            arrayConstructor: Uint8Array,
        },
        "|u1": {
            name: "uint8",
            size: 8,
            arrayConstructor: Uint8Array,
        },
        "<u2": {
            name: "uint16",
            size: 16,
            arrayConstructor: Uint16Array,
        },
        "|i1": {
            name: "int8",
            size: 8,
            arrayConstructor: Int8Array,
        },
        "<i2": {
            name: "int16",
            size: 16,
            arrayConstructor: Int16Array,
        },
        "<u4": {
            name: "uint32",
            size: 32,
            arrayConstructor: Int32Array,
        },
        "<i4": {
            name: "int32",
            size: 32,
            arrayConstructor: Int32Array,
        },
        // "<u8": {
        //     name: "uint64",
        //     size: 64,
        //     arrayConstructor: BigUint64Array,
        // },
        // "<i8": {
        //     name: "int64",
        //     size: 64,
        //     arrayConstructor: BigInt64Array,
        // },
        "<f4": {
            name: "float32",
            size: 32,
            arrayConstructor: Float32Array
        },
        "<f8": {
            name: "float64",
            size: 64,
            arrayConstructor: Float64Array
        },
    };

    this.parse = function(arrayBufferContents) {
        // const version = arrayBufferContents.slice(6, 8); // Uint8-encoded
        const headerLength = new DataView(arrayBufferContents.slice(8, 10)).getUint8(0);
        const offsetBytes = 10 + headerLength;

        let hcontents = new TextDecoder("utf-8").decode(
            new Uint8Array(arrayBufferContents.slice(10, 10 + headerLength))
        );
        var header = JSON.parse(
            hcontents
                .replace(/'/g, '"')
                .replace("False", "false")
                .replace("(", "[")
                .replace(/,*\),*/g, "]")
        );
        var shape = header.shape;

        let dtype = this.dtypes[header.descr];

        let nums = new dtype["arrayConstructor"](
            arrayBufferContents,
            offsetBytes
        );

        return {
            dtype: dtype.name,
            data: nums,
            shape
        };
    }

    this.load = function(filename, callback) {
        /*
        Loads an array from a stream of bytes.
        */
        let self = this;
        return fetch(filename).then(fh => {
            if (fh.ok) {
                return fh.blob().then(i => {
                    var content = i;
                    var reader = new FileReader();
                    // reader.addEventListener("loadend", function () {
                    // 	var text = reader.result;
                    // 	var res = self.parse(text);
                    // 	if (callback) {
                    // 		return callback(res);
                    // 	}
                    // 	return res;
                    // });
                    // alert(content);
                    reader.readAsArrayBuffer(content);
                    reader.onload = function(){
                        var rawLog = reader.result;
                        return callback(self.parse(rawLog));
                    }

                    
                }).catch(err => console.error(err));
            }
        }).catch(err => console.error(err));
    }	
}

// module.exports = npyjs