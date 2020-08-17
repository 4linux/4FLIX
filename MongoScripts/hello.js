c = new Mongo(ip);
db = c.getDB("dexter");
//db.funcionarios.insert({"nome":"fulano"});
funcs = db.funcionarios.find();
while(funcs.hasNext()){
	printjson(funcs.next());
}
