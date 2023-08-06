{# USES_VARIABLES { _synaptic_pre, _synaptic_post, rand,
                    N_incoming, N_outgoing, N,
                    N_pre, N_post, _source_offset, _target_offset } #}
{# WRITES_TO_READ_ONLY_VARIABLES { N_incoming, N_outgoing}
#}

#include "brianlib/common_math.h"
#include "brianlib/stdint_compat.h"
#include<cmath>
#include<ctime>
#include<iostream>
#include<fstream>
#include<climits>
#include "brianlib/stdint_compat.h"
#include "synapses_classes.h"

////// SUPPORT CODE ///////
namespace {{codeobj_name}}_generator {
	{{support_code_lines|autoindent}}
}

////// HASH DEFINES ///////
{{hashdefine_lines|autoindent}}

void _run_{{codeobj_name}}()
{
    using namespace brian;
    using namespace  {{codeobj_name}}_generator;

    ///// CONSTANTS ///////////
    %CONSTANTS%

    ///// POINTERS ////////////
    {{pointers_lines|autoindent}}
	
    {# Get N_post and N_pre in the correct way, regardless of whether they are
    constants or scalar arrays#}
    const size_t _N_pre = {{constant_or_scalar('N_pre', variables['N_pre'])}};
    const size_t _N_post = {{constant_or_scalar('N_post', variables['N_post'])}};
    {{_dynamic_N_incoming}}.resize(_N_post + _target_offset);
    {{_dynamic_N_outgoing}}.resize(_N_pre + _source_offset);
    size_t _raw_pre_idx, _raw_post_idx;
    // scalar code
    const int _vectorisation_idx = -1;
    {{scalar_code['setup_iterator']|autoindent}}
    {{scalar_code['create_j']|autoindent}}
    {{scalar_code['create_cond']|autoindent}}
    {{scalar_code['update_post']|autoindent}}
    for(size_t _i=0; _i<_N_pre; _i++)
    {
        bool __cond, _cond;
        _raw_pre_idx = _i + _source_offset;
        {% if not postsynaptic_condition %}
        {
            {{vector_code['create_cond']|autoindent}}
            __cond = _cond;
        }
        _cond = __cond;
        if(!_cond) continue;
        {% endif %}
        // Some explanation of this hackery. The problem is that we have multiple code blocks.
        // Each code block is generated independently of the others, and they declare variables
        // at the beginning if necessary (including declaring them as const if their values don't
        // change). However, if two code blocks follow each other in the same C++ scope then
        // that causes a redeclaration error. So we solve it by putting each block inside a
        // pair of braces to create a new scope specific to each code block. However, that brings
        // up another problem: we need the values from these code blocks. I don't have a general
        // solution to this problem, but in the case of this particular template, we know which
        // values we need from them so we simply create outer scoped variables to copy the value
        // into. Later on we have a slightly more complicated problem because the original name
        // _j has to be used, so we create two variables __j, _j at the outer scope, copy
        // _j to __j in the inner scope (using the inner scope version of _j), and then
        // __j to _j in the outer scope (to the outer scope version of _j). This outer scope
        // version of _j will then be used in subsequent blocks.
        long _uiter_low;
        long _uiter_high;
        long _uiter_step;
        {% if iterator_func=='sample' %}
        double _uiter_p;
        {% endif %}
        {
            {{vector_code['setup_iterator']|autoindent}}
            _uiter_low = _iter_low;
            _uiter_high = _iter_high;
            _uiter_step = _iter_step;
            {% if iterator_func=='sample' %}
            _uiter_p = _iter_p;
            {% endif %}
        }
        {% if iterator_func=='range' %}
        for(long {{iteration_variable}}=_uiter_low; {{iteration_variable}}<_uiter_high; {{iteration_variable}}+=_uiter_step)
        {
        {% elif iterator_func=='sample' %}
        if(_uiter_p==0) continue;
        const bool _jump_algo = _uiter_p<0.25;
        double _log1p;
        if(_jump_algo)
            _log1p = log(1-_uiter_p);
        else
            _log1p = 1.0; // will be ignored
        const double _pconst = 1.0/log(1-_uiter_p);
        for(long {{iteration_variable}}=_uiter_low; {{iteration_variable}}<_uiter_high; {{iteration_variable}}++)
        {
            if(_jump_algo) {
                const double _r = _rand(_vectorisation_idx);
                if(_r==0.0) break;
                const int _jump = floor(log(_r)*_pconst)*_uiter_step;
                {{iteration_variable}} += _jump;
                if({{iteration_variable}}>=_uiter_high) continue;
            } else {
                if(_rand(_vectorisation_idx)>=_uiter_p) continue;
            }
        {% endif %}
            long __j, _j, _pre_idx, __pre_idx;
            {
                {{vector_code['create_j']|autoindent}}
                __j = _j; // pick up the locally scoped _j and store in __j
                __pre_idx = _pre_idx;
            }
            _j = __j; // make the previously locally scoped _j available
            _pre_idx = __pre_idx;
            _raw_post_idx = _j + _target_offset;
            {% if postsynaptic_condition %}
            {
                {% if postsynaptic_variable_used %}
                {# The condition could index outside of array range #}
                if(_j<0 || _j>=_N_post)
                {
                    {% if skip_if_invalid %}
                    continue;
                    {% else %}
                    cout << "Error: tried to create synapse to neuron j=" << _j << " outside range 0 to " <<
                                            _N_post-1 << endl;
                    exit(1);
                    {% endif %}
                }
                {% endif %}
                {{vector_code['create_cond']|autoindent}}
                __cond = _cond;
            }
            _cond = __cond;
            {% endif %}

            {% if if_expression!='True' %}
            if(!_cond) continue;
            {% endif %}
            {% if not postsynaptic_variable_used %}
            {# Otherwise, we already checked before #}
            if(_j<0 || _j>=_N_post)
            {
                {% if skip_if_invalid %}
                continue;
                {% else %}
                cout << "Error: tried to create synapse to neuron j=" << _j << " outside range 0 to " <<
                        _N_post-1 << endl;
                exit(1);
                {% endif %}
            }
            {% endif %}
            {{vector_code['update_post']|autoindent}} 
	    
	    for (size_t _repetition=0; _repetition<_n; _repetition++) {
	        {{_dynamic_N_outgoing}}[_pre_idx] += 1;
	        {{_dynamic_N_incoming}}[_post_idx] += 1;
	    }
	  }
        }
    
}
