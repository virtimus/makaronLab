#include <QApplication>
#include <QObject>
#include <QStyleFactory>
#include <iostream>

#include <spaghetti/editor.h>
#include <spaghetti/registry.h>

int main(int argc, char **argv)
{
  QApplication app{ argc, argv };
  app.setStyle(QStyleFactory::create("Fusion"));

  QPalette darkPalette;
  QColor c1 = QColor(55, 55, 55);
  QColor c2 = QColor(25, 25, 25);
  QColor c3 = QColor(45, 130, 220);
  darkPalette.setColor(QPalette::Window, c1);
  darkPalette.setColor(QPalette::WindowText, Qt::white);
  darkPalette.setColor(QPalette::Base, c2);
  darkPalette.setColor(QPalette::AlternateBase, c1);
  darkPalette.setColor(QPalette::ToolTipBase, Qt::white);
  darkPalette.setColor(QPalette::ToolTipText, Qt::white);
  darkPalette.setColor(QPalette::Text, Qt::white);
  darkPalette.setColor(QPalette::Button, c1);
  darkPalette.setColor(QPalette::ButtonText, Qt::white);
  darkPalette.setColor(QPalette::BrightText, Qt::red);
  darkPalette.setColor(QPalette::Link, c3);
  darkPalette.setColor(QPalette::Highlight, c3);
  darkPalette.setColor(QPalette::HighlightedText, Qt::white);
  app.setPalette(darkPalette);
  app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }");

  std::locale::global(std::locale("C"));

  auto &registry = spaghetti::Registry::instance();
  registry.registerInternalElements();
  registry.loadPlugins();
  registry.loadPackages();

  spaghetti::Editor editor{ nullptr, &registry };
  QObject::connect(&app, &QApplication::aboutToQuit, &editor, &spaghetti::Editor::aboutToQuit);
  editor.show();
  // editor.showMaximized();

  return app.exec();
}
