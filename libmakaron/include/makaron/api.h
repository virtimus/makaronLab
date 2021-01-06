#pragma once
#ifndef MAKARON_API_H
#define MAKARON_API_H
#include <spaghetti/element.h>
#include <spaghetti/editor.h>
#include <spaghetti/registry.h>
#include <spaghetti/strings.h>
#include <spaghetti/logger.h>
#include "nodes/package.h"//spaghetti
#include <shared_library.h>
#include <spaghetti/vendor/json.hpp>

#define MAKARON_API __attribute__((visibility("default")))

#define MLAB_TMP 1
#define MLAB_OLD 1

namespace makaron {
	namespace log = spaghetti::log;

	using Json = nlohmann::json;

	//using log = spaghetti::log;
	//using apiBaseRegistry = spaghetti::Registry;// base class for registry
	//using apiBaseEditor = spaghetti::Editor;// base class for editor
	namespace string {

		constexpr size_t length(char const *const string)
		{
		  return *string ? 1 + length(string + 1) : 0;
		}
		using hash_t = uint32_t;
		constexpr hash_t FNV_OFFSET{ 0x811c9dc5u };
		constexpr hash_t FNV_PRIME{ 0x01000193u };
		//const auto length = spaghetti::string::length;
		//const auto hash = spaghetti::string::hash;
		constexpr hash_t hash(char const *const a_key, hash_t const &a_offset = FNV_OFFSET, hash_t const &a_prime = FNV_PRIME)
		{
		  hash_t value{ a_offset };
		  size_t const size{ length(a_key) };
		  for (size_t i = 0; i < size; ++i) {
		    value ^= static_cast<hash_t>(a_key[i]);
		    value *= a_prime;
		  }

		  return value;
		}
	}

	//used in editor
	//class Package;
	using Element = spaghetti::Element;
	using GItem = Element;
	using Package = spaghetti::Package;
	//class Package;
	//using Package = spaghetti::Package;
	using Graph = Package;

	class GraphInfo;
	using PackageInfo = GraphInfo;
	//class PackageView;
	//using PackageView = spaghetti::PackageView;
	//class PackageView;
	//using GraphView = PackageView;
	class GraphView;
	using PackageView = GraphView;
	//using PackageView = spaghetti::PackageView;
	//using ElementsList = spaghetti::ElementsList;
	//using NodesList = ElementsList;

	//graphview
	//using NodesListModel = spaghetti::NodesListModel;
	//using Node = spaghetti::Node;
	class GraphNode;
	namespace nodes {
	//	using Package = spaghetti::nodes::Package;
		//class Node;
		using Package = makaron::GraphNode;
	}
	//using GraphNode = nodes::Package;
	class Node;
	//using LinkItem = spaghetti::LinkItem;
	using ValueType = spaghetti::ValueType;
	//using SocketItem = spaghetti::SocketItem;
	class SocketItem;
	class LinkItem;
	using SocketItemType = spaghetti::SocketItemType;
	//using Element = spaghetti::Element;
	using Event = spaghetti::Event;
	using EventType = spaghetti::EventType;
    using IOSocketsType = spaghetti::IOSocketsType;
    using EventIONameChanged = spaghetti::EventIONameChanged;
    using EventIOTypeChanged = spaghetti::EventIOTypeChanged;
    using EventNameChanged = spaghetti::EventNameChanged;
    using EventConsoleTrig = spaghetti::EventConsoleTrig;
    using EOrientation = spaghetti::EOrientation;


    class GVItem;
    class GElem;
    //using SharedLibrary = spaghetti::SharedLibrary;
    //using Plugins = std::vector<std::shared_ptr<SharedLibrary>>;
}//namespace makaron


#endif // MAKARON_API_H
