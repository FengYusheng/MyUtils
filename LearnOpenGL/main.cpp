#include <QtWidgets\qapplication.h>

#include <FirstGLWindow.h>

int main(int argc, char* argv[])
{
	QApplication app(argc, argv);

	FirstGLWindow glWindow;
	
	glWindow.show();

	return app.exec();
}