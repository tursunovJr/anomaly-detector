from enum import Enum

class Operator(Enum):
  intersection = "INTER"
  union = "UNION"
  difference = "DIFF"
  include = "INCL"
  negative = "NEG"

class METRIC_ID(Enum):
  methods_number = "NMD"
  incoming_reference_num = "NIR"
  outcoming_reference_num = "NOR"
  coupling = "CPL"
  cohesion = "COH"
  method_param_avg_num = "ANP"
  primitive_type_param_avg_num = "ANPT"
  accessor_methods_avg_num = "ANAM"
  identical_methods_avg_num = "ANIM"
  invocations_num = "NMI"
  invoked_transitive_methods_num = "NTMI"
  response_time = "RT"
  availability = "A"
  encapsulated_services_num = "NSE"
  total_param_num = "TNP"
  interfaces_num = "NI"
  utility_methods_num = "NUM"
  payload = "PLD"

class Comparator(Enum):
  equal = "equal"
  less = "less"
  less_equal = "less_equal"
  greater = "greater"
  greater_equal = "greater_equal"

class Ordi_Value(Enum):
  very_low = "very_low"
  low = "low"
  medium = "medium"
  high = "high"
  very_high = "very_high"

class Antipattern(Enum):
  BottleneckService = [METRIC_ID.response_time, METRIC_ID.availability, METRIC_ID.coupling]
  ChattyService = [METRIC_ID.invocations_num, METRIC_ID.response_time, METRIC_ID.payload]
  DataService = [METRIC_ID.method_param_avg_num, METRIC_ID.primitive_type_param_avg_num, METRIC_ID.accessor_methods_avg_num, METRIC_ID.cohesion]
  DuplicatedService = [METRIC_ID.identical_methods_avg_num]
  MultiService = [METRIC_ID.methods_number, METRIC_ID.response_time, METRIC_ID.availability, METRIC_ID.cohesion]
  NobodyHome = [METRIC_ID.incoming_reference_num, METRIC_ID.invocations_num]
  ServiceChain = [METRIC_ID.invoked_transitive_methods_num, METRIC_ID.availability]
  TheKnot = [METRIC_ID.coupling, METRIC_ID.cohesion, METRIC_ID.availability, METRIC_ID.response_time]
  TinyService = [METRIC_ID.methods_number, METRIC_ID.coupling]
  # OverEngineering = []
  LostDataService = [METRIC_ID.response_time, METRIC_ID.availability] 

class Antipatterns(Enum):
   BottleneckService = 'BottleneckService'
   ChattyService = 'ChattyService'
   DuplicatedService = 'DuplicatedService'
   LostDataService = 'LostDataService'
   NobodyHome = 'NobodyHome'
   ServiceChain = 'ServiceChain'