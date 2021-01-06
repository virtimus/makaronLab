#include "spaghetti/element.h"
#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"
#include <QtConcurrent/QtConcurrent>

#include "Chips.h"
#include "CPCPC.h"
#include "CPCPCNode.h"
//#include "api.h"
//#include "run.h"

//extern "C" void cpc_run(unsigned int wid);
//extern int cpc_run(int argc, char **argv);

//extern int cpc_run(WId wid);
extern "C" int cpc_run(int argc, unsigned int wid);
extern "C" void setRootWid(unsigned int wid);
extern "C" unsigned int getRootWid();
static spaghetti::Registry *__registry;
namespace makaron::chips {

Chips::Chips() : spaghetti::Element{}
{
    //setRootWid(__registry->wId());
	QFuture<void>  m_f1  = QtConcurrent::run(cpc_run,1,getRootWid());
}



extern "C" SPAGHETTI_API void register_plugin(spaghetti::Registry &registry)
{
  spaghetti::log::init_from_plugin();
  //cpc_run();

  //char *argv[0];//
  //QFuture<void>  m_f1  = QtConcurrent::run(cpc_run,1,registry.wId());
  //__registry = &registry;
  setRootWid(registry.wId());

  registry.registerElement<CPCPC,CPCPCNode>("CPCPC", ":/unknown.png");

}




} //namespace makaron::chips



