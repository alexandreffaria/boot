function getCharacter(boss) {
    var level;
    if (boss) {
        level = 99;
    }
    return {
        name: "Goblin",
        level: level, // Uh-oh! level is `number | undefined`
    };
}
var goblin = getCharacter(false);
console.log(goblin.level + 1);
