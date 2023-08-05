# JsonFS

a horrible idea

ᵖʸᵖᶦ ᵐᵃᵈᵉ ᵐᵉ ʳᵉⁿᵃᵐᵉ ᶦᵗ ˢᵐʰ

## usage

```python
import BetterJsonFS
jsfs = BetterJsonFS.jsonfs()

#write a file into fs
with open("otherstuff/KEKW.png", "rb") as f:
    jsfs.write("/KEKW.png", f.read())
    f.close()

#check if the file exists in fs
print(jsfs.checkifexists("/KEKW.png"))

#write file from fs
with open("fstest.png", "wb") as f:
    f.write(jsfs.read("/KEKW.png"))
    f.close()

#remove from fs
jsfs.remove("/KEKW.png")
```

## Installing

make sure you have python pip installed

if you can use bash you can install it via `pip install betterjsonfs`
