//
// Created by liquidcore7 on 5/7/17.
//

#include "imageServer.hpp"


position::position(int mapx, int mapy, int usrx, int usry) {
	mapPos.first = mapx;
	mapPos.second = mapy;
	usrPos.first = usrx;
	usrPos.second = usry;
}

std::ostream& operator<<(std::ostream& os, const position &pos)
{
	os << pos.getMap().first << " " << pos.getMap().second << " " <<
	   pos.getUsr().first << " " <<
	   pos.getUsr().second;
	return os;
}

position::operator std::string() const
{
	std::ostringstream oss;
	oss << *this;
	return oss.str();
}

std::string imageServer::runPy(const std::vector<std::string> &parsedReq,
                               functional::MODE md)
{
	if (md == functional::SPAWN)
	{
		std::string filename = parsedReq[0] + "150150";
		position spawned(imageServer::random() % 600 + 1000,
		                 imageServer::random() % 500 + 750, 150, 150);
		positions.insert({parsedReq[0], spawned});
		std::string map = spawned;
		system(("python3 srv.py spawn " + map + " " + filename).c_str());
		return _serv_ip + filename + ".jpg";
	} else {
		std::string pos = positions[parsedReq[0]],
				filename = parsedReq[0] + std::to_string(random() % 200);
		system(("python3 srv.py move " + pos + " " + parsedReq[1] + " " + parsedReq[2]
		        + " " + filename).c_str());
		// position on map + user position + x-axis direction + y-axis direction
		// new position
		positions[parsedReq[0]].usrPos.first += 20 * std::stoi(parsedReq[1]);
		positions[parsedReq[0]].usrPos.second += 20 * std::stoi(parsedReq[2]);
		return _serv_ip + filename + ".jpg";
	}
}

imageServer::imageServer(const int port) : servInstance(new Server)
{
	servInstance->config.port = port;
	// regex: /move/1+_digits/digit_with_optional_minus_sign/digit_with_optional_minus_sign
	servInstance->resource["^/move/([0-9]+)/-?\\d/-?\\d$"]["GET"] =
			[this](std::shared_ptr<Server::Response> response,
			   std::shared_ptr<Server::Request> request)
			{
				// usrid = user_id, x = x-axis direction, y = y-axis direction
				auto usrid = request->path.substr(6), x = usrid.substr(usrid.find('/') + 1),
				y = x.substr(x.find('/') + 1);
				std::vector<std::string> content = {usrid.substr(0, usrid.find('/')),
				                                    x.substr(0, x.find('/')), y};
				std::string responseData = runPy(content);
				*response << "HTTP/1.1 200 OK\r\nContent-Length: " <<
				                                                   responseData.length() << "\r\n\r\n"
			                                                        << responseData;
			};
	servInstance->resource["^/spawn/([0-9]+)$"]["GET"] =
		[this] (std::shared_ptr<Server::Response> response,
		    std::shared_ptr<Server::Request> request)
		{
			std::vector<std::string> usrID = {request->path_match[1]};
			std::string responseData = runPy(usrID, functional::SPAWN);
			*response << "HTTP/1.1 200 OK\r\nContent-Length: " <<
		              responseData.length() << "\r\n\r\n" << responseData;
		};
	// ends game for usrid
	servInstance->resource["^/end/([0-9]+)$"]["GET"] =
	[this] (std::shared_ptr<Server::Response> response,
	        std::shared_ptr<Server::Request> request)
	{
		this->positions.erase(request->path_match[1]);
		std::string responseData("user deleted");
		*response << "HTTP/1.1 200 OK\r\nContent-Length: " <<
	              responseData.length() << "\r\n\r\n" << responseData;
	};
	// TODO: remove this testing stuff
	servInstance->resource["^/echo$"]["POST"] =
	[] (std::shared_ptr<Server::Response> response,
	    std::shared_ptr<Server::Request> request)
	{
		std::string responseData = request->content.string();
		if (responseData.empty())
			responseData = "Hello, World!";
		*response << "HTTP/1.1 200 OK\r\nContent-Length: " <<
	              responseData.length() << "\r\n\r\n" << responseData;
	};
}

imageServer::~imageServer() {
	this->stop();
}