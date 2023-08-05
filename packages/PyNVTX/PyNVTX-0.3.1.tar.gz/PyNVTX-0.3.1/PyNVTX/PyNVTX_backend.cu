#include <nvToolsExt.h>
#include <pybind11/pybind11.h>


namespace py = pybind11;


PYBIND11_MODULE(PyNVTX_backend, m) {
    m.def(
        "RangePush",
        [](const char * label) {
            nvtxRangePush(label);
        }
    );

    m.def(
        "RangePushA",
        [](const char * label) {
            nvtxRangePushA(label);
        }
    );

    m.def(
        "RangePop",
        []() {
            nvtxRangePop();
        }
    );

    m.attr("backend_major_version")   = py::int_(0);
    m.attr("backend_minor_version")   = py::int_(2);
    m.attr("backend_release_version") = py::int_(0);

    // Let the user know that this backend has been compiled _with_ CUDA support
    m.attr("cuda_enabled")            = py::bool_(true);
}
