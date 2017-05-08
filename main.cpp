#include "imageServer.hpp"

int main() {
	imageServer server(8080);
	server.run();
	return 0;
}