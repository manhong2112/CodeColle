require("Set")

class NilClass
   def run
      return nil
   end

   def let
      return nil
   end

   def apply
      return nil
   end

   def also
      return nil
   end
end

class Object
   # T.run(() -> k) -> k
   def run(&b)
      instance_eval &b
   end

   # T.let((T) -> k) -> k
   def let(&_)
      yield self
   end

   # T.apply(() -> k) -> T
   def apply(&b)
      instance_eval &b
      self
   end

   # T.also((T) -> k) -> T
   def also(&_)
      yield self
      self
   end
end

class String
   def to_underscore!
      gsub!(/(.)([A-Z])/,'\1_\2')
      downcase!
   end

   def to_underscore
      dup.tap { |s| s.to_underscore! }
   end
end

def record(name, *attr)
   name = name.to_sym
   Struct.new(:$datatype, :$name, *attr) do
      def is_a?(datatype_or_record)
         # datatype_or_record : data(...) | record(...)
         return (send(:$datatype) == datatype_or_record.send(:$name) rescue false) ||
                  (super(datatype_or_record.send(:$struct)) rescue false)
      end
   end.let do |s|
      l = lambda do |*args|
         raise ArgumentError unless attr.length == args.length
         s.new((l.send(:$datatype).send(:$name) rescue nil), l.send(:$name), *args)
      end.apply do
         self.define_singleton_method("$name") do
            name
         end
         self.define_singleton_method("$datatype") do
            nil
         end
         self.define_singleton_method("$is_record_constructor?") do
            true
         end
         self.define_singleton_method("$struct") do
            s
         end
      end
      .also do |l|
         Object.const_set(name, l)
         self.define_singleton_method(name, &l)
      end
   end
end

def data(name, *records)
   name = name.to_sym
   datatype = RecordType(records).apply {
      Object.const_set(name, self)
      class << self
         attr_reader :impls
      end
      @impls = {}
      self.define_singleton_method(:impl) do
         |interface, &block|
         pack = pack_define_method(&block)
         raise TypeError, "Not enough method, missing #{interface.pack.methods_hole - pack.methods}" if pack.methods < interface.pack.methods_hole

         self.impls[interface.send(:$name)] = pack
         records.each do |r|
            s = r.send(:$struct)
            interface.pack.methods.each do |m|
               s.define_method(m) {
                  |*args| interface.pack.send(m, self, *args)
               }
            end
            pack.methods.each do |m|
               s.define_method(m) {
                  |*args| pack.send(m, self, *args)
               }
            end
         end
      end
   }
   records.each do |i|
      i.define_singleton_method("$datatype") do
         datatype
      end
   end
   nil
end

def interface(name, &block)
   name = name.to_sym

   # init
   if not(Object.const_defined? name)
      i = Interface(MethodPack.new)
      Object.const_set(name, i)
   end
   # type check
   raise ArgumentError unless Object.const_get(name).is_a?(Interface)

   method_pack = Object.const_get(name).pack
   method_pack.instance_eval(&block)
   nil
end

record(:Interface, :pack)
record(:RecordType, :records)

class MethodPack
   attr_accessor :methods, :methods_hole
   def initialize
      self.methods = Set.new
      self.methods_hole = Set.new
   end
   def with_method(*name)
      self.methods += name
      self.methods_hole += name
   end
   def singleton_method_added(name)
      self.methods.add(name)
      self.methods_hole.delete(name)
   end
end

def pack_define_method(&block)
   MethodPack.new.apply {
      instance_eval(&block)
   }
end

interface(:Eq) do
   with_method :==, :!=
   def ==(x, y)
      !(x != y)
   end
   def !=(x, y)
      !(x == y)
   end
end

interface(:Match) do
   with_method :match
end
