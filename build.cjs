const fs=require('node:fs'),path=require('node:path');
const read=n=>fs.readFileSync(path.join(__dirname,'src',n),'utf8');
const engine=read('engine.js'),app=read('app.js');let html=read('index.html');
for(const [token,value] of [['{{ENGINE}}',engine],['{{APP}}',app]]){
 if(html.split(token).length!==2)throw Error('Expected exactly one '+token);
 if(/<\/script/i.test(value))throw Error('Closing script tag in source');
 html=html.replace(token,()=>value);
}
fs.mkdirSync(path.join(__dirname,'dist'),{recursive:true});
for(const [name,data] of [['index.html',html],['engine.js',engine],['app.js',app]])fs.writeFileSync(path.join(__dirname,'dist',name),data);
console.log('Built dist/ from src/');
