- **v0.0.1**
    - first version, starting with tagging


- **v0.0.2**
    - 901a45c introducing shiny constructor for shacol class and main method
    - 5b7d982 introducing new method findCollisionWithDBSet using Redis sets, not fast as expected
    - 03412e8 Ready for global hash input with -hg arg. Added the most perfomance function that is able to find a collision up to the 3 bilions with function above in short time. New hashes for testing.
    - e055c69 line reduction of the storing alg. for servermethod
    - e188d48 changed way of computing collision-hash-index number
    - c868d2b created changelog, first version
    - 397456d Solve the bugs with SetArray, but still more time consuming than Server method.
