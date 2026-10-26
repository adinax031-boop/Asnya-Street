const http=require('node:http'),fs=require('node:fs/promises'),path=require('node:path');
const allowed=new Map([['/','index.html'],['/index.html','index.html'],['/engine.js','engine.js'],['/app.js','app.js']]);
function createServer(){return http.createServer(async(req,res)=>{
 if(!['GET','HEAD'].includes(req.method)){res.writeHead(405,{'Allow':'GET, HEAD'});return res.end()}
 let file;try{file=allowed.get(new URL(req.url,'http://localhost').pathname)}catch{res.writeHead(400);return res.end()}
 if(!file){res.writeHead(404);return res.end('Not found')}
 try{const data=await fs.readFile(path.join(__dirname,'dist',file));res.writeHead(200,{'Content-Type':file.endsWith('.html')?'text/html; charset=utf-8':'text/javascript; charset=utf-8','X-Content-Type-Options':'nosniff','Cache-Control':'no-store','Content-Length':data.length});res.end(req.method==='HEAD'?undefined:data)}catch{res.writeHead(500);res.end('Run npm run build first')}
})}
if(require.main===module){const port=Number(process.env.PORT||4173);if(!Number.isInteger(port)||port<1||port>65535)throw Error('Invalid PORT');const server=createServer();server.on('error',e=>{console.error(e.message);process.exitCode=1});server.listen(port,'127.0.0.1',()=>console.log('http://127.0.0.1:'+port));for(const sig of ['SIGINT','SIGTERM'])process.on(sig,()=>server.close())}
module.exports={createServer};
