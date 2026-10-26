const {test}=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
test('browser bundle initializes research and handles portfolio demo and stress events',()=>{
 const elements=new Map(),storage=new Map();
 const defaults={fast:'20',slow:'60',cost:'5',strategy:'trend',dataset:'trend','shock-percent':'-20','shock-target':'all'};
 function el(id){if(!elements.has(id))elements.set(id,{value:defaults[id]||'',innerHTML:'',textContent:'',classList:{toggle(){}},querySelector(){return null},querySelectorAll(){return []},add(){},replaceChildren(){},focus(){},reset(){}});return elements.get(id)}
 const document={getElementById:el,querySelectorAll(){return []},addEventListener(){},createElement(){return {click(){}}}};
 const context=vm.createContext({document,window:{},localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},Option:function(label,value){this.label=label;this.value=value},Intl,Blob,URL,setTimeout});
 const html=fs.readFileSync(__dirname+'/dist/index.html','utf8');
 for(const [,script] of html.matchAll(/<script>([\s\S]*?)<\/script>/g))vm.runInContext(script,context);
 assert(el('metrics').innerHTML.includes('Total return'));assert(el('runmsg').textContent.startsWith('Complete'));
 el('portfolio-demo').onclick();assert(el('portfolio-metrics').innerHTML.includes('$11,100.00'));assert(el('positions').innerHTML.includes('DEMO-A'));
 el('shock-form').onsubmit({preventDefault(){}});assert(el('shock-result').innerHTML.includes('$9,280.00'));assert(el('shock-result').innerHTML.includes('-$1,820.00'));
 context.window.showTab('portfolio');assert.equal(el('crumb').textContent,'Portfolio desk');assert(storage.has('asnya-portfolio-v1'));
});
