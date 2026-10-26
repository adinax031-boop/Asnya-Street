const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),{execFileSync}=require('node:child_process'),{Script}=require('node:vm'),{createServer}=require('./serve.cjs');
test('build is deterministic, complete and valid JavaScript',()=>{
 const p=path.join(__dirname,'dist/index.html'),a=fs.readFileSync(p,'utf8');execFileSync(process.execPath,['build.cjs'],{cwd:__dirname});assert.equal(fs.readFileSync(p,'utf8'),a);assert(!a.includes('{{ENGINE}}'));assert(!a.includes('{{APP}}'));
 const scripts=[...a.matchAll(/<script>([\s\S]*?)<\/script>/g)];assert.equal(scripts.length,2);for(const [,js]of scripts)new Script(js);assert(a.includes("getElementById('command-run')"));assert.equal(fs.readFileSync(path.join(__dirname,'dist/app.js'),'utf8'),fs.readFileSync(path.join(__dirname,'src/app.js'),'utf8'));
});
test('HTTP serving rejects private paths and write methods',async t=>{
 const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));t.after(()=>new Promise(r=>server.close(r)));const url='http://127.0.0.1:'+server.address().port;
 const page=await fetch(url);assert.equal(page.status,200);assert((await page.text()).includes('Asnya Street'));assert.equal((await fetch(url+'/engine.js')).headers.get('content-type'),'text/javascript; charset=utf-8');assert.equal((await fetch(url+'/.git/config')).status,404);assert.equal((await fetch(url+'/README.md')).status,404);assert.equal((await fetch(url,{method:'POST'})).status,405);assert.equal(await(await fetch(url,{method:'HEAD'})).text(),'');
});
