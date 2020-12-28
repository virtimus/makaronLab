#include <cstdlib>
#include <iostream>
//#include <QtConcurrent>
#include <QtConcurrent/QtConcurrent>
#include "spaghetti/element.h"
#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"

extern int main(int argc, char **argv);

class TinyEMU final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "_tinyEmu/TinyEMU" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };

  TinyEMU()
    : spaghetti::Element{}
  {
	  char *argv[0];
	  m_f1  = QtConcurrent::run(main,0,(char**)&argv);

  }

  ~TinyEMU()
  {
	  m_f1.cancel();
  }

  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

 private:
  QFuture<void> m_f1;


};



extern "C" SPAGHETTI_API void register_plugin(spaghetti::Registry &a_registry)
{
  //spaghetti::log::init_from_plugin();

  a_registry.registerElement<TinyEMU>("tinyEmu ", ":/unknown.png");
}
