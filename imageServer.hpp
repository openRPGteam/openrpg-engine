//
// Created by liquidcore7 on 5/7/17.
//

#ifndef OPENRPG_ENGINE_SERVER_IMAGESERVER_HPP
#define OPENRPG_ENGINE_SERVER_IMAGESERVER_HPP

#include <memory>
#include "server_http.hpp"
#include <map>
#include <random>

typedef SimpleWeb::Server<SimpleWeb::HTTP> Server;


namespace functional
{
	enum MODE {SPAWN, MOVE};
}

class imageServer;

class position {
public:
	std::pair<int, int> mapPos;
	std::pair<int, int> usrPos;
public:
	position() = default;
	position(int, int, int, int);
	inline auto getMap() const { return mapPos;}
	inline auto getUsr() const { return usrPos;}
	operator std::string() const;
};

std::ostream& operator<<(std::ostream&, const position &);

class imageServer {
private:
	std::unique_ptr<Server> servInstance;
	std::string runPy(const std::vector<std::string>&, functional::MODE = functional::MOVE);
	std::map<std::string, position> positions;
	std::random_device random;
public:
	imageServer(const int = 8080);
	inline void run() {servInstance->start();}
	inline void stop() {servInstance->stop();}
	~imageServer();
};


#endif //OPENRPG_ENGINE_SERVER_IMAGESERVER_HPP
