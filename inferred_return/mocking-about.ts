type Character = {
  name: string;
  level: number;
};

function getCharacter(boss: boolean): Character {
  let level: number;

   if (boss) {
     level = 99;
   }

   return {
     name: "Goblin",
     level: level, // Uh-oh! level is `number | undefined`
   };
 }

let goblin = getCharacter(false)

console.log(goblin.level + 1)
